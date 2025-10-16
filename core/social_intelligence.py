"""
Social Intelligence Module - Social media reconnaissance
"""

import requests
from datetime import datetime
import json
import re

class SocialIntelligence:
    def __init__(self, config):
        self.config = config
        self.platforms = [
            'github', 'twitter', 'instagram', 'facebook', 'linkedin',
            'reddit', 'pinterest', 'youtube', 'tiktok', 'snapchat',
            'medium', 'devto', 'stackoverflow', 'gitlab', 'bitbucket'
        ]
        
    def search_username(self, username):
        results = {
            'username': username,
            'timestamp': datetime.now().isoformat(),
            'platforms_found': [],
            'profiles': {}
        }
        
        for platform in self.platforms:
            profile = self.check_platform(username, platform)
            if profile['exists']:
                results['platforms_found'].append(platform)
                results['profiles'][platform] = profile
        
        return results
    
    def check_platform(self, username, platform):
        urls = {
            'github': f'https://github.com/{username}',
            'twitter': f'https://twitter.com/{username}',
            'instagram': f'https://instagram.com/{username}',
            'facebook': f'https://facebook.com/{username}',
            'linkedin': f'https://linkedin.com/in/{username}',
            'reddit': f'https://reddit.com/user/{username}',
            'pinterest': f'https://pinterest.com/{username}',
            'youtube': f'https://youtube.com/@{username}',
            'tiktok': f'https://tiktok.com/@{username}',
            'medium': f'https://medium.com/@{username}',
            'devto': f'https://dev.to/{username}',
            'stackoverflow': f'https://stackoverflow.com/users/{username}',
            'gitlab': f'https://gitlab.com/{username}',
            'bitbucket': f'https://bitbucket.org/{username}'
        }
        
        url = urls.get(platform, '')
        
        try:
            response = requests.get(url, timeout=5, headers={'User-Agent': self.config.get('user_agent')})
            
            if response.status_code == 200:
                return {
                    'exists': True,
                    'url': url,
                    'status_code': response.status_code,
                    'data': self.extract_profile_data(response.text, platform)
                }
            else:
                return {
                    'exists': False,
                    'url': url,
                    'status_code': response.status_code
                }
        except Exception as e:
            return {
                'exists': False,
                'url': url,
                'error': str(e)
            }
    
    def extract_profile_data(self, html, platform):
        data = {}
        
        if platform == 'github':
            name_match = re.search(r'<span.*?itemprop="name".*?>(.*?)</span>', html)
            if name_match:
                data['name'] = name_match.group(1).strip()
            
            bio_match = re.search(r'<div.*?class=".*?user-profile-bio.*?".*?>(.*?)</div>', html)
            if bio_match:
                data['bio'] = bio_match.group(1).strip()
        
        return data
    
    def search_across_platforms(self, query):
        results = {}
        for platform in self.platforms:
            results[platform] = self.platform_search(query, platform)
        return results
    
    def platform_search(self, query, platform):
        return {
            'query': query,
            'platform': platform,
            'results': []
        }
    
    def analyze_activity(self, username, platform):
        return {
            'username': username,
            'platform': platform,
            'posts': [],
            'followers': 0,
            'following': 0,
            'engagement_rate': 0
        }
    
    def find_related_accounts(self, username):
        return {
            'username': username,
            'related': [],
            'connections': []
        }
