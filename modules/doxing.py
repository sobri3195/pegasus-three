"""
Doxing Module - Advanced information aggregation
WARNING: This module must be used legally and ethically only
"""

from datetime import datetime
import json

class DoxingModule:
    def __init__(self, config):
        self.config = config
        self.disclaimer_shown = False
        
    def show_disclaimer(self):
        if not self.disclaimer_shown:
            print("\n" + "="*70)
            print("⚠️  LEGAL WARNING ⚠️")
            print("="*70)
            print("This module aggregates public information only.")
            print("You MUST have legal authorization to investigate targets.")
            print("Unauthorized doxing is ILLEGAL and punishable by law.")
            print("Use this tool responsibly and ethically.")
            print("="*70 + "\n")
            self.disclaimer_shown = True
    
    def aggregate_information(self, target_data):
        self.show_disclaimer()
        
        dossier = {
            'timestamp': datetime.now().isoformat(),
            'personal_info': self.extract_personal_info(target_data),
            'digital_footprint': self.analyze_digital_footprint(target_data),
            'contact_methods': self.aggregate_contacts(target_data),
            'locations': self.extract_locations(target_data),
            'associations': self.find_associations(target_data),
            'timeline': self.build_timeline(target_data),
            'risk_indicators': self.identify_risks(target_data),
            'data_sources': self.list_sources(target_data)
        }
        
        return dossier
    
    def extract_personal_info(self, data):
        personal = {
            'names': set(),
            'aliases': set(),
            'usernames': set(),
            'bio': [],
            'occupation': [],
            'education': []
        }
        
        if 'social' in data:
            social_data = data['social']
            if 'username' in social_data:
                personal['usernames'].add(social_data['username'])
            
            for platform, profile in social_data.get('profiles', {}).items():
                if 'data' in profile:
                    if 'name' in profile['data']:
                        personal['names'].add(profile['data']['name'])
                    if 'bio' in profile['data']:
                        personal['bio'].append(profile['data']['bio'])
        
        if 'email' in data:
            email_format = data['email'].get('format', {})
            username = email_format.get('username', '')
            if username:
                personal['usernames'].add(username)
        
        return {
            'names': list(personal['names']),
            'aliases': list(personal['aliases']),
            'usernames': list(personal['usernames']),
            'bio': personal['bio'],
            'occupation': personal['occupation'],
            'education': personal['education']
        }
    
    def analyze_digital_footprint(self, data):
        footprint = {
            'social_platforms': [],
            'websites': [],
            'domains': [],
            'email_addresses': [],
            'phone_numbers': [],
            'activity_level': 'unknown'
        }
        
        if 'social' in data:
            footprint['social_platforms'] = data['social'].get('platforms_found', [])
        
        if 'osint' in data:
            footprint['domains'].append(data['osint'].get('target'))
            footprint['websites'].extend(data['osint'].get('subdomains', []))
        
        if 'email' in data:
            footprint['email_addresses'].append(data['email'].get('email'))
        
        if 'phone' in data:
            footprint['phone_numbers'].append(data['phone'].get('phone_number'))
        
        platform_count = len(footprint['social_platforms'])
        if platform_count > 5:
            footprint['activity_level'] = 'high'
        elif platform_count > 2:
            footprint['activity_level'] = 'medium'
        elif platform_count > 0:
            footprint['activity_level'] = 'low'
        
        return footprint
    
    def aggregate_contacts(self, data):
        contacts = {
            'emails': [],
            'phones': [],
            'social_handles': {},
            'messaging_apps': []
        }
        
        if 'email' in data:
            email_info = data['email']
            contacts['emails'].append({
                'address': email_info.get('email'),
                'valid': email_info.get('valid', {}).get('valid', False),
                'breach_status': email_info.get('breach_check', {}).get('found', False)
            })
        
        if 'phone' in data:
            phone_info = data['phone']
            contacts['phones'].append({
                'number': phone_info.get('phone_number'),
                'valid': phone_info.get('validation', {}).get('valid', False),
                'carrier': phone_info.get('carrier_info', {}).get('carrier'),
                'type': phone_info.get('validation', {}).get('number_type')
            })
        
        if 'social' in data:
            social_data = data['social']
            username = social_data.get('username')
            for platform in social_data.get('platforms_found', []):
                contacts['social_handles'][platform] = username
        
        return contacts
    
    def extract_locations(self, data):
        locations = {
            'ip_locations': [],
            'phone_locations': [],
            'metadata_locations': [],
            'social_locations': []
        }
        
        if 'osint' in data:
            ip_info = data['osint'].get('ip_info', {})
            geo = ip_info.get('geolocation', {})
            if geo:
                locations['ip_locations'].append({
                    'country': geo.get('country_name'),
                    'city': geo.get('city'),
                    'region': geo.get('region'),
                    'latitude': geo.get('latitude'),
                    'longitude': geo.get('longitude')
                })
        
        if 'phone' in data:
            phone_location = data['phone'].get('location', {})
            if phone_location.get('location'):
                locations['phone_locations'].append({
                    'location': phone_location['location'],
                    'country_code': phone_location.get('country_code')
                })
        
        if 'metadata' in data:
            meta = data['metadata'].get('metadata', {})
            if 'Location' in meta:
                locations['metadata_locations'].append(meta['Location'])
        
        return locations
    
    def find_associations(self, data):
        associations = {
            'linked_accounts': [],
            'shared_identifiers': [],
            'connected_domains': [],
            'related_entities': []
        }
        
        if 'email' in data and 'osint' in data:
            email_domain = data['email'].get('email', '').split('@')[-1]
            target_domain = data['osint'].get('target', '')
            
            if email_domain and target_domain and email_domain == target_domain:
                associations['connected_domains'].append({
                    'relationship': 'email_domain_match',
                    'entities': [email_domain, target_domain]
                })
        
        if 'social' in data:
            platforms = data['social'].get('platforms_found', [])
            if len(platforms) > 1:
                associations['linked_accounts'].append({
                    'username': data['social'].get('username'),
                    'platforms': platforms
                })
        
        return associations
    
    def build_timeline(self, data):
        events = []
        
        if 'osint' in data:
            whois_data = data['osint'].get('whois', {})
            if 'creation_date' in whois_data:
                events.append({
                    'date': whois_data['creation_date'],
                    'event': 'Domain registered',
                    'source': 'WHOIS',
                    'details': whois_data.get('registrar')
                })
        
        if 'metadata' in data:
            basic_info = data['metadata'].get('basic_info', {})
            if 'created' in basic_info:
                events.append({
                    'date': basic_info['created'],
                    'event': 'File created',
                    'source': 'File metadata',
                    'details': data['metadata'].get('file_name')
                })
        
        events.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        return events
    
    def identify_risks(self, data):
        risks = {
            'privacy_risks': [],
            'security_risks': [],
            'exposure_level': 'unknown'
        }
        
        if 'email' in data:
            if data['email'].get('breach_check', {}).get('found'):
                risks['security_risks'].append({
                    'type': 'data_breach',
                    'severity': 'high',
                    'description': 'Email found in data breaches'
                })
        
        if 'social' in data:
            platform_count = len(data['social'].get('platforms_found', []))
            if platform_count > 5:
                risks['privacy_risks'].append({
                    'type': 'high_exposure',
                    'severity': 'medium',
                    'description': f'Active on {platform_count} social platforms'
                })
        
        if 'network' in data:
            open_ports = len(data['network'].get('ports', {}).get('open_ports', []))
            if open_ports > 5:
                risks['security_risks'].append({
                    'type': 'open_ports',
                    'severity': 'high',
                    'description': f'{open_ports} open ports detected'
                })
        
        total_risks = len(risks['privacy_risks']) + len(risks['security_risks'])
        if total_risks > 3:
            risks['exposure_level'] = 'high'
        elif total_risks > 1:
            risks['exposure_level'] = 'medium'
        elif total_risks > 0:
            risks['exposure_level'] = 'low'
        
        return risks
    
    def list_sources(self, data):
        sources = []
        
        for key in data.keys():
            sources.append({
                'source': key,
                'data_quality': 'available'
            })
        
        return sources
