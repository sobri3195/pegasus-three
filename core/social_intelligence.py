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
            'reddit', 'pinterest', 'youtube', 'tiktok',
            'medium', 'devto', 'stackoverflow', 'gitlab', 'bitbucket'
        ]
        self.platform_rules = {
            'github': {'avatar_selector': 'meta property="og:image"', 'rate_limit_hint': '60/min'},
            'twitter': {'avatar_selector': 'profile_image_url', 'rate_limit_hint': 'varies'},
        }
        
    def _http_get(self, url, timeout=5):
        headers = {'User-Agent': self.config.get('user_agent')}
        proxies = {'http': self.config.get('proxy'), 'https': self.config.get('proxy')} if self.config.get('proxy') else None
        return requests.get(url, timeout=timeout, headers=headers, proxies=proxies)
        
    def search_username(self, username):
        results = {
            'username': username,
            'timestamp': datetime.now().isoformat(),
            'platforms_found': [],
            'profiles': {},
            'graph': {}
        }
        
        for platform in self.platforms:
            profile = self.check_platform(username, platform)
            if profile['exists']:
                results['platforms_found'].append(platform)
                results['profiles'][platform] = profile
        
        results['graph'] = self.build_profile_graph(results)
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
            response = self._http_get(url, timeout=6)
            
            if response.status_code == 200:
                data = self.extract_profile_data(response.text, platform)
                data['avatar_url'] = self.extract_avatar_url(response.text, platform)
                data['keywords'] = self.tag_bio_keywords(data.get('bio', '')) if data.get('bio') else []
                data['screenshot'] = self.generate_screenshot_link(url)
                return {
                    'exists': True,
                    'url': url,
                    'status_code': response.status_code,
                    'data': data
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
    
    def extract_avatar_url(self, html, platform):
        # Heuristic extraction
        m = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']', html, re.IGNORECASE)
        if m:
            return m.group(1)
        m = re.search(r'avatar_url["\']?\s*[:=]\s*["\']([^"\']+)["\']', html, re.IGNORECASE)
        return m.group(1) if m else None
    
    def build_profile_graph(self, results):
        nodes = []
        edges = []
        username = results.get('username')
        for platform in results.get('platforms_found', []):
            nodes.append({'id': f'{platform}:{username}', 'label': platform})
            edges.append({'from': username, 'to': f'{platform}:{username}', 'type': 'account'})
        return {'nodes': nodes, 'edges': edges}
    
    def tag_bio_keywords(self, bio):
        keywords = ['security', 'developer', 'hacker', 'engineer', 'researcher']
        tags = [k for k in keywords if k.lower() in bio.lower()]
        return tags
    
    def suggest_usernames(self, username):
        variants = [
            f"{username}_", f"_{username}", f"{username}123", f"{username}.dev", f"real_{username}"
        ]
        return variants
    
    def detect_throwaway_platform(self, platform):
        return platform in ['tiktok']
    
    def estimate_account_creation_date(self, platform, html):
        return None
    
    def generate_screenshot_link(self, url):
        return f"https://image.thum.io/get/width/1200/{url}"
    
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
