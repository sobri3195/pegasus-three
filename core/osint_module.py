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
        
    def _http_get(self, url, allow_redirects=True, timeout=None, stream=False):
        import time
        retries = int(self.config.get('retries', 2))
        backoff = float(self.config.get('backoff_factor', 0.5))
        timeout = timeout or int(self.config.get('timeout', 10))
        headers = {'User-Agent': self.config.get('user_agent', 'Pegasus-OSINT/1.0')}
        proxies = {'http': self.config.get('proxy'), 'https': self.config.get('proxy')} if self.config.get('proxy') else None
        rate_limit = float(self.config.get('rate_limit', 0))
        last_ex = None
        for attempt in range(retries + 1):
            try:
                if rate_limit and attempt == 0:
                    time.sleep(1.0 / max(rate_limit, 1))
                resp = requests.get(url, timeout=timeout, allow_redirects=allow_redirects, headers=headers, proxies=proxies, stream=stream)
                if resp.status_code == 429 and attempt < retries:
                    time.sleep(backoff * (2 ** attempt))
                    continue
                return resp
            except Exception as e:
                last_ex = e
                time.sleep(backoff * (2 ** attempt))
        raise last_ex if last_ex else Exception('HTTP request failed')
        
    def scan(self, target):
        self.results = {
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'whois': self.whois_lookup(target),
            'dns': self.dns_enumeration(target),
            'dnssec': self.detect_dnssec(target),
            'subdomains': self.find_subdomains(target),
            'ip_info': self.get_ip_info(target),
            'ssl_info': self.get_ssl_info(target),
            'headers': self.get_http_headers(target)
        }
        if self.config.get('deep_scan'):
            self.results['advanced'] = self.deep_scan_features(target)
        return self.results
    
    def deep_scan_features(self, target):
        info = {}
        info['http_versions'] = self.detect_http_versions(target)
        info['cdn'] = self.detect_cdn(target)
        info['waf'] = self.detect_waf(target)
        info['robots'] = self.fetch_robots_security(target)
        info['sitemap'] = self.fetch_sitemap(target)
        info['tls'] = self.enumerate_tls(target)
        info['hsts'] = self.check_hsts(target)
        info['open_redirect'] = self.check_open_redirects(target)
        info['email_auth'] = self.analyze_email_auth(target)
        info['cors'] = self.inspect_cors(target)
        info['csp'] = self.inspect_csp(target)
        info['tech_fingerprint'] = self.fingerprint_tech(target)
        info['favicon'] = self.favicon_hash(target)
        info['admin_paths'] = self.probe_admin_paths(target)
        info['canonical'] = self.extract_canonical_url(target)
        info['reverse_whois'] = self.reverse_whois(target)
        return info
    
    def whois_lookup(self, domain):
        try:
            w = whois.whois(domain)
            abuse_contact = None
            emails = w.emails
            if isinstance(emails, list):
                for e in emails:
                    if 'abuse' in str(e).lower():
                        abuse_contact = e
                        break
            elif isinstance(emails, str) and 'abuse' in emails.lower():
                abuse_contact = emails
            return {
                'domain_name': w.domain_name,
                'registrar': w.registrar,
                'creation_date': str(w.creation_date),
                'expiration_date': str(w.expiration_date),
                'name_servers': w.name_servers,
                'status': w.status,
                'emails': emails,
                'abuse_contact': abuse_contact,
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
    
    def detect_dnssec(self, domain):
        status = {'dnskey': False, 'ds': False}
        try:
            answers = dns.resolver.resolve(domain, 'DNSKEY')
            status['dnskey'] = len(list(answers)) > 0
        except Exception:
            pass
        try:
            answers = dns.resolver.resolve(domain, 'DS')
            status['ds'] = len(list(answers)) > 0
        except Exception:
            pass
        status['enabled'] = status['dnskey'] and status['ds']
        return status
    
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
            try:
                hostname = socket.gethostbyaddr(ip)[0]
            except Exception:
                hostname = None
            
            try:
                response = self._http_get(f'https://ipapi.co/{ip}/json/', timeout=5)
                geo_data = response.json()
            except Exception:
                geo_data = {}
            
            return {
                'ip_address': ip,
                'hostname': hostname,
                'geolocation': geo_data,
                'asn': geo_data.get('asn') if isinstance(geo_data, dict) else None
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
            
            response = self._http_get(target, timeout=10, allow_redirects=True)
            
            return {
                'url': target,
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'cookies': dict(response.cookies),
                'redirects': [r.url for r in response.history]
            }
        except Exception as e:
            return {'error': str(e)}
    
    def detect_http_versions(self, target):
        info = {'http2': False, 'http3': False}
        try:
            if not target.startswith('http'):
                target = f'https://{target}'
            resp = self._http_get(target, timeout=10)
            alt_svc = resp.headers.get('alt-svc', '')
            if 'h3' in alt_svc:
                info['http3'] = True
            # Heuristic for HTTP/2
            via = resp.headers.get('via', '')
            if 'h2' in alt_svc or 'HTTP/2' in via:
                info['http2'] = True
        except Exception:
            pass
        return info
    
    def detect_cdn(self, target):
        providers = ['cloudflare', 'akamai', 'fastly', 'cloudfront']
        detected = None
        try:
            headers = self.get_http_headers(target).get('headers', {})
            server = str(headers.get('server', '')).lower()
            via = str(headers.get('via', '')).lower()
            cf = headers.get('cf-ray') or headers.get('cf-cache-status')
            x_cache = headers.get('x-cache')
            for p in providers:
                if p in server or p in via:
                    detected = p
                    break
            if cf:
                detected = 'cloudflare'
            if x_cache and 'cloudfront' in str(x_cache).lower():
                detected = 'cloudfront'
        except Exception:
            pass
        return {'provider': detected}
    
    def detect_waf(self, target):
        waf_headers = ['x-sucuri-id', 'x-sucuri-block', 'x-mod-security', 'x-firewall', 'cf-ray']
        try:
            headers = self.get_http_headers(target).get('headers', {})
            indicators = {h: headers.get(h) for h in waf_headers if headers.get(h)}
            return {'detected': len(indicators) > 0, 'indicators': indicators}
        except Exception:
            return {'detected': False}
    
    def fetch_robots_security(self, target):
        result = {}
        base = target if target.startswith('http') else f'https://{target}'
        for path in ['/robots.txt', '/.well-known/security.txt']:
            url = f'{base}{path}'
            try:
                resp = self._http_get(url, timeout=5)
                if resp.status_code < 400:
                    result[path] = {'status': resp.status_code, 'length': len(resp.text), 'sample': resp.text[:200]}
                else:
                    result[path] = {'status': resp.status_code}
            except Exception as e:
                result[path] = {'error': str(e)}
        return result
    
    def fetch_sitemap(self, target):
        base = target if target.startswith('http') else f'https://{target}'
        url = f'{base}/sitemap.xml'
        try:
            resp = self._http_get(url, timeout=5)
            if resp.status_code < 400:
                text = resp.text
                urls = re.findall(r'<loc>(.*?)</loc>', text)
                return {'status': resp.status_code, 'url_count': len(urls), 'sample_urls': urls[:10]}
            return {'status': resp.status_code}
        except Exception as e:
            return {'error': str(e)}
    
    def enumerate_tls(self, target):
        # Basic probe of negotiated protocol/cipher
        info = {'protocol': None, 'cipher': None}
        try:
            import ssl
            host = target
            if host.startswith('http'):
                host = host.split('://', 1)[1].split('/', 1)[0]
            context = ssl.create_default_context()
            with socket.create_connection((host, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    info['protocol'] = ssock.version()
                    info['cipher'] = ssock.cipher()[0] if ssock.cipher() else None
        except Exception as e:
            info['error'] = str(e)
        return info
    
    def check_hsts(self, target):
        try:
            headers = self.get_http_headers(target).get('headers', {})
            hsts = headers.get('strict-transport-security') or headers.get('Strict-Transport-Security')
            return {'enabled': bool(hsts), 'preload': 'preload' in str(hsts).lower() if hsts else False}
        except Exception as e:
            return {'error': str(e)}
    
    def check_open_redirects(self, target):
        # Heuristic checks for common open redirect parameters
        base = target if target.startswith('http') else f'https://{target}'
        candidates = [
            f'{base}/?next=http://example.com',
            f'{base}/redirect?url=http://example.com',
            f'{base}/out?url=http://example.com'
        ]
        findings = []
        for url in candidates:
            try:
                resp = self._http_get(url, allow_redirects=False, timeout=5)
                loc = resp.headers.get('Location') or resp.headers.get('location')
                if loc and 'example.com' in loc:
                    findings.append({'url': url, 'status': resp.status_code, 'location': loc})
            except Exception:
                continue
        return {'potential': len(findings) > 0, 'samples': findings[:2]}
    
    def analyze_email_auth(self, domain):
        # SPF, DKIM (selector-agnostic), DMARC
        result = {'spf': None, 'dmarc': None, 'dkim': None}
        try:
            txt = dns.resolver.resolve(domain, 'TXT')
            spf = [str(rdata.strings[0].decode()) if hasattr(rdata, 'strings') and rdata.strings else str(rdata) for rdata in txt]
            spf_records = [t for t in spf if 'v=spf1' in t]
            result['spf'] = spf_records[0] if spf_records else None
        except Exception:
            result['spf'] = None
        try:
            dmarc_domain = f'_dmarc.{domain}'
            txt = dns.resolver.resolve(dmarc_domain, 'TXT')
            dmarc = [str(rdata.strings[0].decode()) if hasattr(rdata, 'strings') and rdata.strings else str(rdata) for rdata in txt]
            dmarc_records = [t for t in dmarc if 'v=DMARC1' in t]
            dmarc_policy = None
            if dmarc_records:
                rec = dmarc_records[0]
                m = re.search(r'p=([a-zA-Z]+)', rec)
                if m:
                    dmarc_policy = m.group(1)
            result['dmarc'] = {'record': dmarc_records[0] if dmarc_records else None, 'policy': dmarc_policy}
        except Exception:
            result['dmarc'] = None
        # DKIM requires selector; provide placeholder
        result['dkim'] = {'note': 'Selector required for DKIM check'}
        return result
    
    def inspect_cors(self, target):
        try:
            headers = self.get_http_headers(target).get('headers', {})
            return {
                'allow_origin': headers.get('Access-Control-Allow-Origin') or headers.get('access-control-allow-origin'),
                'allow_credentials': headers.get('Access-Control-Allow-Credentials') or headers.get('access-control-allow-credentials')
            }
        except Exception as e:
            return {'error': str(e)}
    
    def inspect_csp(self, target):
        try:
            headers = self.get_http_headers(target).get('headers', {})
            csp = headers.get('Content-Security-Policy') or headers.get('content-security-policy')
            return {'configured': bool(csp), 'policy': csp}
        except Exception as e:
            return {'error': str(e)}
    
    def fingerprint_tech(self, target):
        fp = {'headers': {}, 'html_signatures': []}
        try:
            base = target if target.startswith('http') else f'https://{target}'
            resp = self._http_get(base, timeout=8)
            headers = {k.lower(): v for k, v in resp.headers.items()}
            fp['headers'] = {k: headers.get(k) for k in ['server', 'x-powered-by', 'via'] if headers.get(k)}
            html = resp.text.lower()
            signatures = {
                'wordpress': 'wp-content',
                'drupal': 'drupal-settings-json',
                'joomla': 'joomla',
                'cloudflare': 'cf-ray',
                'nginx': 'nginx',
                'apache': 'apache'
            }
            for name, sig in signatures.items():
                if sig in html or (fp['headers'].get('server') and name in fp['headers'].get('server','').lower()):
                    fp['html_signatures'].append(name)
        except Exception:
            pass
        return fp
    
    def favicon_hash(self, target):
        import hashlib
        base = target if target.startswith('http') else f'https://{target}'
        url = f'{base}/favicon.ico'
        try:
            resp = self._http_get(url, timeout=5, stream=True)
            if resp.status_code < 400:
                content = resp.content if hasattr(resp, 'content') else resp.raw.read(4096)
                return {'md5': hashlib.md5(content).hexdigest(), 'size': len(content)}
        except Exception as e:
            return {'error': str(e)}
        return {'message': 'favicon not available'}
    
    def probe_admin_paths(self, target):
        paths = ['admin', 'administrator', 'login', 'wp-admin', 'cpanel']
        base = target if target.startswith('http') else f'https://{target}'
        findings = []
        for p in paths:
            url = f'{base}/{p}'
            try:
                resp = self._http_get(url, timeout=5, allow_redirects=False)
                if resp.status_code in (200, 301, 302, 401, 403):
                    findings.append({'path': f'/{p}', 'status': resp.status_code})
            except Exception:
                continue
        return findings
    
    def extract_canonical_url(self, target):
        try:
            base = target if target.startswith('http') else f'https://{target}'
            resp = self._http_get(base, timeout=8)
            m = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', resp.text, re.IGNORECASE)
            return {'canonical': m.group(1) if m else None}
        except Exception as e:
            return {'error': str(e)}
    
    def reverse_whois(self, domain):
        return {'message': 'Reverse WHOIS requires external service', 'supported': False}
