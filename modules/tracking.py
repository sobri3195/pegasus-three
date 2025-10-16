"""
Tracking Module - Monitor and track digital activities
WARNING: Must be used with proper legal authorization only
"""

from datetime import datetime, timedelta
import json
import hashlib

class TrackingModule:
    def __init__(self, config):
        self.config = config
        self.tracking_data = {}
        
    def create_tracking_profile(self, target_id, target_data):
        profile = {
            'target_id': target_id,
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'baseline': self.create_baseline(target_data),
            'monitoring_points': self.identify_monitoring_points(target_data),
            'alert_rules': self.define_alert_rules(),
            'history': []
        }
        
        return profile
    
    def create_baseline(self, data):
        baseline = {
            'timestamp': datetime.now().isoformat(),
            'social_presence': {},
            'domain_status': {},
            'email_status': {},
            'network_status': {}
        }
        
        if 'social' in data:
            baseline['social_presence'] = {
                'platforms': data['social'].get('platforms_found', []),
                'profile_count': len(data['social'].get('platforms_found', []))
            }
        
        if 'osint' in data:
            baseline['domain_status'] = {
                'domain': data['osint'].get('target'),
                'ip': data['osint'].get('ip_info', {}).get('ip_address'),
                'ssl_valid': 'ssl_info' in data['osint']
            }
        
        if 'email' in data:
            baseline['email_status'] = {
                'email': data['email'].get('email'),
                'valid': data['email'].get('valid', {}).get('valid', False),
                'in_breach': data['email'].get('breach_check', {}).get('found', False)
            }
        
        if 'network' in data:
            baseline['network_status'] = {
                'open_ports': len(data['network'].get('ports', {}).get('open_ports', [])),
                'services': [p['service'] for p in data['network'].get('ports', {}).get('open_ports', [])]
            }
        
        return baseline
    
    def identify_monitoring_points(self, data):
        points = []
        
        if 'social' in data:
            for platform in data['social'].get('platforms_found', []):
                profile_url = data['social'].get('profiles', {}).get(platform, {}).get('url')
                points.append({
                    'type': 'social_profile',
                    'platform': platform,
                    'url': profile_url,
                    'check_interval': 3600
                })
        
        if 'osint' in data:
            domain = data['osint'].get('target')
            points.append({
                'type': 'domain',
                'target': domain,
                'check_interval': 86400
            })
        
        if 'email' in data:
            email = data['email'].get('email')
            points.append({
                'type': 'email',
                'target': email,
                'check_interval': 604800
            })
        
        return points
    
    def define_alert_rules(self):
        rules = [
            {
                'rule_id': 'new_social_account',
                'description': 'Alert when new social media account is detected',
                'severity': 'medium',
                'enabled': True
            },
            {
                'rule_id': 'domain_change',
                'description': 'Alert when domain registration changes',
                'severity': 'high',
                'enabled': True
            },
            {
                'rule_id': 'new_breach',
                'description': 'Alert when email appears in new breach',
                'severity': 'high',
                'enabled': True
            },
            {
                'rule_id': 'network_change',
                'description': 'Alert when network configuration changes',
                'severity': 'medium',
                'enabled': True
            },
            {
                'rule_id': 'location_change',
                'description': 'Alert when location data changes',
                'severity': 'low',
                'enabled': True
            }
        ]
        
        return rules
    
    def compare_snapshots(self, baseline, current):
        changes = {
            'timestamp': datetime.now().isoformat(),
            'changes_detected': [],
            'change_count': 0,
            'severity': 'none'
        }
        
        if baseline.get('social_presence', {}).get('platforms') != current.get('social_presence', {}).get('platforms'):
            old_platforms = set(baseline.get('social_presence', {}).get('platforms', []))
            new_platforms = set(current.get('social_presence', {}).get('platforms', []))
            
            added = new_platforms - old_platforms
            removed = old_platforms - new_platforms
            
            if added:
                changes['changes_detected'].append({
                    'type': 'social_account_added',
                    'platforms': list(added),
                    'severity': 'medium'
                })
            
            if removed:
                changes['changes_detected'].append({
                    'type': 'social_account_removed',
                    'platforms': list(removed),
                    'severity': 'low'
                })
        
        if baseline.get('domain_status', {}).get('ip') != current.get('domain_status', {}).get('ip'):
            changes['changes_detected'].append({
                'type': 'ip_change',
                'old_ip': baseline.get('domain_status', {}).get('ip'),
                'new_ip': current.get('domain_status', {}).get('ip'),
                'severity': 'high'
            })
        
        if not baseline.get('email_status', {}).get('in_breach') and current.get('email_status', {}).get('in_breach'):
            changes['changes_detected'].append({
                'type': 'new_breach_detected',
                'email': current.get('email_status', {}).get('email'),
                'severity': 'high'
            })
        
        if baseline.get('network_status', {}).get('open_ports') != current.get('network_status', {}).get('open_ports'):
            changes['changes_detected'].append({
                'type': 'network_configuration_change',
                'old_ports': baseline.get('network_status', {}).get('open_ports'),
                'new_ports': current.get('network_status', {}).get('open_ports'),
                'severity': 'medium'
            })
        
        changes['change_count'] = len(changes['changes_detected'])
        
        if any(c['severity'] == 'high' for c in changes['changes_detected']):
            changes['severity'] = 'high'
        elif any(c['severity'] == 'medium' for c in changes['changes_detected']):
            changes['severity'] = 'medium'
        elif changes['change_count'] > 0:
            changes['severity'] = 'low'
        
        return changes
    
    def track_activity_pattern(self, target_id, activity_data):
        pattern = {
            'target_id': target_id,
            'timestamp': datetime.now().isoformat(),
            'activity_type': activity_data.get('type'),
            'frequency': self.calculate_frequency(target_id, activity_data),
            'peak_times': self.identify_peak_times(target_id),
            'platforms_used': activity_data.get('platforms', []),
            'behavior_analysis': self.analyze_behavior(activity_data)
        }
        
        return pattern
    
    def calculate_frequency(self, target_id, activity_data):
        return {
            'daily_average': 0,
            'weekly_average': 0,
            'trend': 'stable'
        }
    
    def identify_peak_times(self, target_id):
        return {
            'most_active_hour': None,
            'most_active_day': None,
            'timezone_estimate': None
        }
    
    def analyze_behavior(self, activity_data):
        return {
            'consistency': 'unknown',
            'predictability': 'unknown',
            'anomalies_detected': []
        }
    
    def generate_movement_timeline(self, location_data):
        timeline = {
            'start_date': None,
            'end_date': None,
            'locations': [],
            'total_distance': 0,
            'countries_visited': set()
        }
        
        for location in location_data:
            timeline['locations'].append({
                'timestamp': location.get('timestamp'),
                'location': location.get('location'),
                'source': location.get('source'),
                'accuracy': location.get('accuracy')
            })
            
            if location.get('country'):
                timeline['countries_visited'].add(location['country'])
        
        timeline['countries_visited'] = list(timeline['countries_visited'])
        
        return timeline
    
    def create_alert(self, alert_type, severity, details):
        alert = {
            'alert_id': hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8],
            'timestamp': datetime.now().isoformat(),
            'type': alert_type,
            'severity': severity,
            'details': details,
            'status': 'new',
            'acknowledged': False
        }
        
        return alert
    
    def export_tracking_report(self, target_id, time_range=None):
        report = {
            'target_id': target_id,
            'generated_at': datetime.now().isoformat(),
            'time_range': time_range or 'all',
            'summary': {},
            'changes': [],
            'alerts': [],
            'recommendations': []
        }
        
        return report
