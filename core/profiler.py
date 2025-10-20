"""
Data Profiler Module - Aggregate and profile information from multiple sources
"""

from datetime import datetime
import json

class DataProfiler:
    def __init__(self, config):
        self.config = config
        
    def create_profile(self, collected_data):
        profile = {
            'timestamp': datetime.now().isoformat(),
            'summary': self.create_summary(collected_data),
            'identity': self.extract_identity_info(collected_data),
            'online_presence': self.extract_online_presence(collected_data),
            'contact_information': self.extract_contact_info(collected_data),
            'technical_footprint': self.extract_technical_info(collected_data),
            'timeline': self.create_timeline(collected_data),
            'relationships': self.map_relationships(collected_data),
            'risk_assessment': self.assess_profile_risk(collected_data),
            'entity_resolution': self.resolve_entities(collected_data),
            'relation_matrix': self.export_relation_matrix(collected_data),
            'confidence_explanation': self.explain_confidence(collected_data),
            'data_sources': list(collected_data.keys())
        }
        
        if self.config.get('report', {}).get('redact', False):
            profile['redacted'] = self.redact_profile(profile)
        
        return profile
    
    def create_summary(self, data):
        summary = {
            'total_sources': len(data),
            'data_quality': self.calculate_data_quality(data),
            'confidence_score': self.calculate_confidence(data),
            'last_updated': datetime.now().isoformat()
        }
        
        if 'osint' in data:
            summary['domain'] = data['osint'].get('target')
        
        if 'social' in data:
            summary['platforms_found'] = len(data['social'].get('platforms_found', []))
        
        if 'email' in data:
            summary['email'] = data['email'].get('email')
        
        if 'phone' in data:
            summary['phone'] = data['phone'].get('phone_number')
        
        return summary
    
    def extract_identity_info(self, data):
        identity = {
            'names': [],
            'usernames': [],
            'aliases': [],
            'emails': [],
            'phone_numbers': [],
            'affiliations': []
        }
        
        if 'social' in data:
            social_data = data['social']
            if 'username' in social_data:
                identity['usernames'].append(social_data['username'])
            
            for platform, profile in social_data.get('profiles', {}).items():
                if 'data' in profile and 'name' in profile['data']:
                    identity['names'].append(profile['data']['name'])
        
        if 'email' in data:
            identity['emails'].append(data['email'].get('email'))
            # Affiliation from email domain
            domain = (data['email'].get('email') or '').split('@')[-1]
            if domain:
                identity['affiliations'].append({'type': 'domain', 'value': domain})
        
        if 'phone' in data:
            identity['phone_numbers'].append(data['phone'].get('phone_number'))
        
        identity['aliases'] = self.discover_aliases(identity)
        identity['names'] = list(set(identity['names']))
        identity['usernames'] = list(set(identity['usernames']))
        identity['emails'] = list(set(identity['emails']))
        identity['phone_numbers'] = list(set(identity['phone_numbers']))
        
        return identity
    
    def extract_online_presence(self, data):
        presence = {
            'social_media': {},
            'websites': [],
            'domains': []
        }
        
        if 'social' in data:
            social_data = data['social']
            for platform in social_data.get('platforms_found', []):
                profile = social_data.get('profiles', {}).get(platform, {})
                presence['social_media'][platform] = {
                    'url': profile.get('url'),
                    'active': profile.get('exists', False)
                }
        
        if 'osint' in data:
            osint_data = data['osint']
            presence['domains'].append(osint_data.get('target'))
            presence['websites'].extend(osint_data.get('subdomains', []))
        
        return presence
    
    def extract_contact_info(self, data):
        contact = {
            'emails': [],
            'phone_numbers': [],
            'addresses': [],
            'social_handles': {}
        }
        
        if 'email' in data:
            email_data = data['email']
            contact['emails'].append({
                'email': email_data.get('email'),
                'valid': email_data.get('valid', {}).get('valid', False),
                'disposable': email_data.get('disposable', {}).get('is_disposable', False)
            })
        
        if 'phone' in data:
            phone_data = data['phone']
            contact['phone_numbers'].append({
                'number': phone_data.get('phone_number'),
                'valid': phone_data.get('validation', {}).get('valid', False),
                'carrier': phone_data.get('carrier_info', {}).get('carrier'),
                'location': phone_data.get('location', {}).get('location')
            })
        
        if 'social' in data:
            social_data = data['social']
            for platform in social_data.get('platforms_found', []):
                contact['social_handles'][platform] = social_data['username']
        
        return contact
    
    def extract_technical_info(self, data):
        technical = {
            'ip_addresses': [],
            'domains': [],
            'technologies': [],
            'ports': []
        }
        
        if 'osint' in data:
            osint_data = data['osint']
            ip_info = osint_data.get('ip_info', {})
            if 'ip_address' in ip_info:
                technical['ip_addresses'].append(ip_info['ip_address'])
            
            technical['domains'].append(osint_data.get('target'))
        
        if 'network' in data:
            network_data = data['network']
            if 'host_info' in network_data:
                technical['ip_addresses'].append(network_data['host_info'].get('ip'))
            
            if 'ports' in network_data:
                ports_info = network_data['ports']
                technical['ports'] = ports_info.get('open_ports', [])
        
        technical['ip_addresses'] = list(set(technical['ip_addresses']))
        technical['domains'] = list(set(technical['domains']))
        
        return technical
    
    def create_timeline(self, data):
        timeline = []
        
        if 'osint' in data:
            osint_data = data['osint']
            whois_data = osint_data.get('whois', {})
            if 'creation_date' in whois_data:
                timeline.append({
                    'date': whois_data['creation_date'],
                    'event': 'Domain registered',
                    'source': 'WHOIS',
                    'confidence': 0.9
                })
        
        if 'metadata' in data:
            meta_data = data['metadata']
            basic_info = meta_data.get('basic_info', {})
            if 'created' in basic_info:
                timeline.append({
                    'date': basic_info['created'],
                    'event': 'File created',
                    'source': 'File Metadata',
                    'confidence': 0.7
                })
        
        timeline.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        return timeline
    
    def map_relationships(self, data):
        relationships = {
            'connections': [],
            'associated_entities': []
        }
        
        if 'social' in data:
            social_data = data['social']
            relationships['connections'].append({
                'type': 'social_media',
                'platforms': social_data.get('platforms_found', [])
            })
        
        if 'email' in data and 'osint' in data:
            email_domain = data['email'].get('email', '').split('@')[-1]
            osint_domain = data['osint'].get('target')
            
            if email_domain == osint_domain:
                relationships['connections'].append({
                    'type': 'domain_association',
                    'entities': [email_domain, osint_domain]
                })
        
        return relationships
    
    def assess_profile_risk(self, data):
        risk_score = 0
        risk_factors = []
        
        if 'email' in data:
            email_data = data['email']
            if email_data.get('breach_check', {}).get('found'):
                risk_score += 30
                risk_factors.append('Email found in data breaches')
            
            if email_data.get('disposable', {}).get('is_disposable'):
                risk_score += 20
                risk_factors.append('Using disposable email')
        
        if 'phone' in data:
            phone_data = data['phone']
            phone_risk = phone_data.get('risk_assessment', {})
            risk_score += phone_risk.get('risk_score', 0) // 2
            risk_factors.extend(phone_risk.get('risk_factors', []))
        
        if 'network' in data:
            network_data = data['network']
            open_ports = len(network_data.get('ports', {}).get('open_ports', []))
            if open_ports > 10:
                risk_score += 25
                risk_factors.append(f'Many open ports detected: {open_ports}')
        
        risk_level = 'LOW'
        if risk_score > 60:
            risk_level = 'HIGH'
        elif risk_score > 30:
            risk_level = 'MEDIUM'
        
        return {
            'risk_score': min(risk_score, 100),
            'risk_level': risk_level,
            'risk_factors': risk_factors
        }
    
    def calculate_data_quality(self, data):
        total_fields = 0
        filled_fields = 0
        
        for source, source_data in data.items():
            if isinstance(source_data, dict):
                for key, value in source_data.items():
                    total_fields += 1
                    if value and value != 'Unknown' and not isinstance(value, dict) or (isinstance(value, dict) and not value.get('error')):
                        filled_fields += 1
        
        quality_score = (filled_fields / total_fields * 100) if total_fields > 0 else 0
        
        return {
            'score': round(quality_score, 2),
            'total_fields': total_fields,
            'filled_fields': filled_fields
        }
    
    def calculate_confidence(self, data):
        confidence = 50
        
        if len(data) > 3:
            confidence += 20
        
        if 'email' in data and data['email'].get('valid', {}).get('valid'):
            confidence += 15
        
        if 'phone' in data and data['phone'].get('validation', {}).get('valid'):
            confidence += 15
        
        return min(confidence, 100)
    
    def explain_confidence(self, data):
        explanation = []
        if 'email' in data and data['email'].get('valid', {}).get('valid'):
            explanation.append('Valid email increases confidence')
        if 'phone' in data and data['phone'].get('validation', {}).get('valid'):
            explanation.append('Valid phone increases confidence')
        if 'social' in data and len(data['social'].get('platforms_found', [])) > 0:
            explanation.append('Active social presence increases confidence')
        return explanation
    
    def resolve_entities(self, data):
        # Simple resolver to deduplicate by canonical forms
        canonical = {}
        if 'identity' in data:
            ident = data['identity']
            canonical['primary_name'] = ident.get('names', [None])[0]
            canonical['primary_email'] = ident.get('emails', [None])[0]
            canonical['primary_phone'] = ident.get('phone_numbers', [None])[0]
        return canonical
    
    def export_relation_matrix(self, data):
        nodes = []
        edges = []
        # Nodes: email, phone, domain
        if 'email' in data and data['email'].get('email'):
            nodes.append({'id': data['email']['email'], 'type': 'email'})
        if 'phone' in data and data['phone'].get('phone_number'):
            nodes.append({'id': data['phone']['phone_number'], 'type': 'phone'})
        if 'osint' in data and data['osint'].get('target'):
            nodes.append({'id': data['osint']['target'], 'type': 'domain'})
        # Edges
        if 'email' in data and 'osint' in data:
            email_domain = data['email'].get('email', '').split('@')[-1]
            if email_domain == data['osint'].get('target'):
                edges.append({'from': data['email']['email'], 'to': data['osint']['target'], 'type': 'domain_association'})
        return {'nodes': nodes, 'edges': edges}
    
    def discover_aliases(self, identity):
        aliases = []
        for name in identity.get('names', []):
            parts = name.split()
            if len(parts) >= 2:
                aliases.append(f"{parts[0]} {parts[-1][0]}.")
        return list(set(aliases))
    
    def redact_profile(self, profile):
        # Redact PII fields for safe sharing
        redacted = json.loads(json.dumps(profile))
        # Mask email and phone
        if 'identity' in redacted:
            redacted['identity']['emails'] = ['***@***'] if redacted['identity'].get('emails') else []
            redacted['identity']['phone_numbers'] = ['+***********'] if redacted['identity'].get('phone_numbers') else []
        return redacted
