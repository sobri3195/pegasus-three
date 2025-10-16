"""
OSINT Module - Domain and IP reconnaissance
"""

import socket
import whois
import dns.resolver
import requests
from datetime import datetime
import subprocess
import re

class OSINTModule:
    def __init__(self, config):
        self.config = config
        self.results = {}
        
    def scan(self, target):
        self.results = {
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'whois': self.whois_lookup(target),
            'dns': self.dns_enumeration(target),
            'subdomains': self.find_subdomains(target),
            'ip_info': self.get_ip_info(target),
            'ssl_info': self.get_ssl_info(target),
            'headers': self.get_http_headers(target)
        }
        return self.results
    
    def whois_lookup(self, domain):
        try:
            w = whois.whois(domain)
            return {
                'domain_name': w.domain_name,
                'registrar': w.registrar,
                'creation_date': str(w.creation_date),
                'expiration_date': str(w.expiration_date),
                'name_servers': w.name_servers,
                'status': w.status,
                'emails': w.emails,
                'org': w.org
            }
        except Exception as e:
            return {'error': str(e)}
    
    def dns_enumeration(self, domain):
        dns_records = {}
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                dns_records[record_type] = [str(rdata) for rdata in answers]
            except Exception:
                dns_records[record_type] = []
        
        return dns_records
    
    def find_subdomains(self, domain):
        subdomains = []
        common_subdomains = [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp',
            'pop', 'ns1', 'webdisk', 'ns2', 'cpanel', 'whm',
            'autodiscover', 'autoconfig', 'm', 'imap', 'test',
            'ns', 'blog', 'pop3', 'dev', 'www2', 'admin',
            'portal', 'ns3', 'dns1', 'api', 'cdn', 'vpn'
        ]
        
        for sub in common_subdomains:
            try:
                full_domain = f"{sub}.{domain}"
                socket.gethostbyname(full_domain)
                subdomains.append(full_domain)
            except socket.gaierror:
                pass
        
        return subdomains
    
    def get_ip_info(self, target):
        try:
            ip = socket.gethostbyname(target)
            hostname = socket.gethostbyaddr(ip)[0]
            
            try:
                response = requests.get(f'https://ipapi.co/{ip}/json/', timeout=5)
                geo_data = response.json()
            except:
                geo_data = {}
            
            return {
                'ip_address': ip,
                'hostname': hostname,
                'geolocation': geo_data
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_ssl_info(self, domain):
        try:
            import ssl
            import OpenSSL
            
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
            return {
                'subject': dict(x[0] for x in cert['subject']),
                'issuer': dict(x[0] for x in cert['issuer']),
                'version': cert['version'],
                'serial_number': cert['serialNumber'],
                'not_before': cert['notBefore'],
                'not_after': cert['notAfter'],
                'san': cert.get('subjectAltName', [])
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_http_headers(self, target):
        try:
            if not target.startswith('http'):
                target = f'https://{target}'
            
            response = requests.get(target, timeout=10, allow_redirects=True)
            
            return {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'cookies': dict(response.cookies),
                'redirects': [r.url for r in response.history]
            }
        except Exception as e:
            return {'error': str(e)}
