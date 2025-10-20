"""
Email Intelligence Module - Email investigation and validation
"""

import re
import dns.resolver
import requests
from datetime import datetime
import hashlib

class EmailIntelligence:
    def __init__(self, config):
        self.config = config
        
    def investigate(self, email):
        results = {
            'email': email,
            'timestamp': datetime.now().isoformat(),
            'valid': self.validate_email(email),
            'domain_info': self.check_domain(email),
            'breach_check': self.check_breaches(email),
            'breach_summary': self.summarize_breaches(email),
            'disposable': self.check_disposable(email),
            'role_account': self.detect_role_account(email),
            'format': self.analyze_format(email),
            'gravatar': self.generate_gravatar_hash(email),
            'email_auth': self.inspect_email_auth(email),
            'mx_analysis': self.analyze_mx(email),
            'catch_all': self.detect_catch_all(email),
            'typo_suggestions': self.suggest_typos(email),
            'smtp_probe': self.simulate_smtp_probe(email) if self.config.get('intrusive_checks') else {'enabled': False},
            'social_profiles': self.find_social_profiles(email)
        }
        return results
    
    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return {
                'valid': False,
                'reason': 'Invalid format'
            }
        
        domain = email.split('@')[1]
        
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            return {
                'valid': True,
                'mx_records': [str(mx.exchange) for mx in mx_records]
            }
        except Exception as e:
            return {
                'valid': False,
                'reason': f'No MX records found: {str(e)}'
            }
    
    def check_domain(self, email):
        domain = email.split('@')[1]
        
        try:
            import whois
            w = whois.whois(domain)
            return {
                'domain': domain,
                'registrar': w.registrar,
                'creation_date': str(w.creation_date),
                'expiration_date': str(w.expiration_date)
            }
        except Exception as e:
            return {
                'domain': domain,
                'error': str(e)
            }
    
    def check_breaches(self, email):
        try:
            api_key = self.config.get('api_keys', {}).get('haveibeenpwned')
            if api_key:
                headers = {
                    'hibp-api-key': api_key,
                    'User-Agent': self.config.get('user_agent', 'Pegasus-OSINT/1.0')
                }
                response = requests.get(
                    f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}',
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    return {
                        'found': True,
                        'breaches': response.json()
                    }
                elif response.status_code == 404:
                    return {
                        'found': False,
                        'message': 'No breaches found'
                    }
        except Exception:
            pass
        
        return {
            'found': None,
            'message': 'API key required for breach check'
        }
    
    def summarize_breaches(self, email):
        details = self.check_breaches(email)
        summary = {'total': 0, 'sources': []}
        if details.get('found') and isinstance(details.get('breaches'), list):
            summary['total'] = len(details['breaches'])
            summary['sources'] = [b.get('Name') for b in details['breaches'] if isinstance(b, dict)]
        return summary
    
    def check_disposable(self, email):
        domain = email.split('@')[1]
        
        disposable_domains = [
            'tempmail.com', 'guerrillamail.com', '10minutemail.com',
            'mailinator.com', 'throwaway.email', 'temp-mail.org',
            'fakeinbox.com', 'trashmail.com', 'yopmail.com', 'mintemail.com',
            'getnada.com', 'dispostable.com', 'sharklasers.com', 'spamgourmet.com'
        ]
        
        return {
            'is_disposable': domain in disposable_domains,
            'domain': domain
        }
    
    def analyze_format(self, email):
        username, domain = email.split('@')
        
        patterns = {
            'firstname.lastname': r'^[a-z]+\.[a-z]+$',
            'firstname_lastname': r'^[a-z]+_[a-z]+$',
            'firstnamelastname': r'^[a-z]+[a-z]+$',
            'firstinitial.lastname': r'^[a-z]\.[a-z]+$',
            'firstname.lastinitial': r'^[a-z]+\.[a-z]$'
        }
        
        detected_pattern = 'custom'
        for pattern_name, pattern in patterns.items():
            if re.match(pattern, username.lower()):
                detected_pattern = pattern_name
                break
        
        return {
            'username': username,
            'domain': domain,
            'pattern': detected_pattern,
            'length': len(username),
            'has_numbers': bool(re.search(r'\d', username)),
            'has_special': bool(re.search(r'[^a-zA-Z0-9]', username))
        }
    
    def find_social_profiles(self, email):
        profiles = []
        
        try:
            response = requests.get(
                'https://api.fullcontact.com/v3/person.enrich',
                headers={'Authorization': f'Bearer {self.config.get("api_keys", {}).get("fullcontact", "")}'},
                json={'email': email},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                profiles = data.get('socialProfiles', [])
        except Exception:
            pass
        
        return profiles
    
    def inspect_email_auth(self, email):
        domain = email.split('@')[1]
        result = {'spf': None, 'dmarc': None, 'dmarc_grade': None}
        try:
            txt = dns.resolver.resolve(domain, 'TXT')
            records = [str(rdata.strings[0].decode()) if hasattr(rdata, 'strings') and rdata.strings else str(rdata) for rdata in txt]
            spf_records = [t for t in records if 'v=spf1' in t]
            result['spf'] = spf_records[0] if spf_records else None
        except Exception:
            result['spf'] = None
        try:
            dmarc_domain = f'_dmarc.{domain}'
            txt = dns.resolver.resolve(dmarc_domain, 'TXT')
            dmarc_records = [str(rdata.strings[0].decode()) if hasattr(rdata, 'strings') and rdata.strings else str(rdata) for rdata in txt]
            dmarc_policy = None
            if dmarc_records:
                rec = dmarc_records[0]
                m = re.search(r'p=([a-zA-Z]+)', rec)
                if m:
                    dmarc_policy = m.group(1)
            grade = 'low'
            if dmarc_policy == 'reject':
                grade = 'high'
            elif dmarc_policy == 'quarantine':
                grade = 'medium'
            result['dmarc'] = {'record': dmarc_records[0] if dmarc_records else None, 'policy': dmarc_policy}
            result['dmarc_grade'] = grade
        except Exception:
            result['dmarc'] = None
            result['dmarc_grade'] = None
        result['dkim'] = {'note': 'Selector required for DKIM check'}
        return result
    
    def analyze_mx(self, email):
        domain = email.split('@')[1]
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            entries = []
            for mx in mx_records:
                preference = getattr(mx, 'preference', 0)
                exchange = str(mx.exchange).rstrip('.')
                provider = None
                if 'google' in exchange:
                    provider = 'Google Workspace'
                elif 'outlook' in exchange or 'office365' in exchange or 'protection.outlook.com' in exchange:
                    provider = 'Microsoft 365'
                elif 'yahoodns' in exchange or 'yahoo' in exchange:
                    provider = 'Yahoo'
                entries.append({'preference': preference, 'exchange': exchange, 'provider': provider})
            entries.sort(key=lambda x: x.get('preference', 0))
            return {'mx': entries}
        except Exception as e:
            return {'error': str(e)}
    
    def detect_catch_all(self, email):
        # Non-intrusive placeholder
        return {'supported': False, 'note': 'Catch-all detection requires SMTP probing'}
    
    def simulate_smtp_probe(self, email):
        # Best-effort safe probe outline, does not send any mail
        return {'enabled': False, 'note': 'SMTP probing disabled by default'}
    
    def generate_gravatar_hash(self, email):
        md5 = hashlib.md5(email.strip().lower().encode()).hexdigest()
        return {'md5': md5, 'url': f'https://www.gravatar.com/avatar/{md5}'}
    
    def detect_role_account(self, email):
        username = email.split('@')[0].lower()
        roles = ['admin', 'info', 'support', 'sales', 'contact', 'help', 'billing']
        return {'is_role': username in roles, 'role': username if username in roles else None}
    
    def suggest_typos(self, email):
        username, domain = email.split('@')
        suggestions = []
        common = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com']
        if domain not in common:
            for c in common:
                if sorted(domain) == sorted(c) or domain.replace('.', '') == c.replace('.', ''):
                    suggestions.append(f'{username}@{c}')
        return suggestions
    
    def generate_email_variations(self, first_name, last_name, domain):
        variations = [
            f'{first_name}.{last_name}@{domain}',
            f'{first_name}_{last_name}@{domain}',
            f'{first_name}{last_name}@{domain}',
            f'{first_name[0]}.{last_name}@{domain}',
            f'{first_name}.{last_name[0]}@{domain}',
            f'{first_name[0]}{last_name}@{domain}',
            f'{last_name}.{first_name}@{domain}',
            f'{last_name}{first_name}@{domain}'
        ]
        
        return [v.lower() for v in variations]
