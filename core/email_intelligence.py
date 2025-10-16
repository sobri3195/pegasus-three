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
            'disposable': self.check_disposable(email),
            'format': self.analyze_format(email),
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
        email_hash = hashlib.sha1(email.encode()).hexdigest()
        
        try:
            api_key = self.config.get('api_keys', {}).get('haveibeenpwned')
            if api_key:
                headers = {
                    'hibp-api-key': api_key,
                    'User-Agent': self.config.get('user_agent')
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
        except Exception as e:
            pass
        
        return {
            'found': None,
            'message': 'API key required for breach check'
        }
    
    def check_disposable(self, email):
        domain = email.split('@')[1]
        
        disposable_domains = [
            'tempmail.com', 'guerrillamail.com', '10minutemail.com',
            'mailinator.com', 'throwaway.email', 'temp-mail.org',
            'fakeinbox.com', 'trashmail.com'
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
                f'https://api.fullcontact.com/v3/person.enrich',
                headers={'Authorization': f'Bearer {self.config.get("api_keys", {}).get("fullcontact", "")}'},
                json={'email': email},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                profiles = data.get('socialProfiles', [])
        except:
            pass
        
        return profiles
    
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
