"""
Network Intelligence Module - Network reconnaissance and port scanning
"""

import socket
import subprocess
from datetime import datetime
import ipaddress
import struct
import select

class NetworkIntelligence:
    def __init__(self, config):
        self.config = config
        self.common_ports = [
            21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443,
            445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443
        ]
        
    def scan(self, target_ip, scan_ports=False):
        results = {
            'target': target_ip,
            'timestamp': datetime.now().isoformat(),
            'host_info': self.get_host_info(target_ip),
            'ping': self.ping_host(target_ip),
            'traceroute': self.traceroute(target_ip)
        }
        
        if scan_ports:
            results['ports'] = self.port_scan(target_ip)
            # Enrich with simple SMB/NetBIOS marker
            results['smb_netbios'] = self.enumerate_smb_netbios(results.get('ports', {}))
        
        if self.config.get('deep_scan'):
            results['advanced'] = {
                'reverse_dns_sweep': self.reverse_dns_sweep(target_ip, limit=16),
                'snmp_public_check': self.snmp_public_check(target_ip),
                'ssh_hostkey_fingerprint': self.ssh_host_key_fingerprint(target_ip),
            }
        
        return results
    
    def get_host_info(self, ip):
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return {
                'ip': ip,
                'hostname': hostname,
                'is_valid': self.validate_ip(ip),
                'private_or_bogon': self.is_private_or_bogon(ip)
            }
        except Exception as e:
            return {
                'ip': ip,
                'hostname': None,
                'error': str(e),
                'is_valid': self.validate_ip(ip),
                'private_or_bogon': self.is_private_or_bogon(ip)
            }
    
    def validate_ip(self, ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    def is_private_or_bogon(self, ip):
        try:
            ip_obj = ipaddress.ip_address(ip)
            return ip_obj.is_private or ip_obj.is_reserved or ip_obj.is_loopback or ip_obj.is_link_local
        except Exception:
            return False
    
    def ping_host(self, target):
        try:
            param = '-n' if subprocess.os.name == 'nt' else '-c'
            command = ['ping', param, '4', target]
            output = subprocess.run(command, capture_output=True, text=True, timeout=10)
            
            return {
                'success': output.returncode == 0,
                'output': output.stdout,
                'response_time': self.parse_ping_time(output.stdout),
                'packet_loss': self.parse_packet_loss(output.stdout)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def parse_ping_time(self, output):
        import re
        time_match = re.search(r'time[=<](\d+\.?\d*)', output)
        if time_match:
            return float(time_match.group(1))
        return None
    
    def parse_packet_loss(self, output):
        import re
        m = re.search(r'(\d+)%\s*packet loss', output)
        if not m:
            m = re.search(r'Lost = \d+ \((\d+)%\)', output)
        return int(m.group(1)) if m else None
    
    def traceroute(self, target):
        try:
            command = ['traceroute', target] if subprocess.os.name != 'nt' else ['tracert', target]
            output = subprocess.run(command, capture_output=True, text=True, timeout=30)
            hops = self.parse_traceroute(output.stdout)
            result = {
                'success': output.returncode == 0,
                'hops': hops
            }
            if self.config.get('deep_scan'):
                result['hop_geolocation'] = self.geolocate_hops(hops)
            return result
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def parse_traceroute(self, output):
        hops = []
        for line in output.split('\n'):
            if line.strip() and not line.startswith('traceroute'):
                hops.append(line.strip())
        return hops
    
    def geolocate_hops(self, hops):
        import re, requests
        geo = []
        for h in hops[:10]:
            ips = re.findall(r'(\d+\.\d+\.\d+\.\d+)', h)
            if not ips:
                continue
            ip = ips[-1]
            try:
                r = requests.get(f'https://ipapi.co/{ip}/json/', timeout=5)
                if r.status_code == 200:
                    data = r.json()
                    geo.append({'ip': ip, 'city': data.get('city'), 'country': data.get('country_name')})
            except Exception:
                continue
        return geo
    
    def port_scan(self, target_ip, ports=None):
        if ports is None:
            ports = self.common_ports
        
        results = {
            'open_ports': [],
            'closed_ports': [],
            'filtered_ports': []
        }
        
        for port in ports:
            status = self.check_port(target_ip, port)
            if status == 'open':
                service = self.identify_service(target_ip, port)
                enriched = self.enrich_service_info(target_ip, port, service)
                results['open_ports'].append({
                    'port': port,
                    'service': enriched
                })
            elif status == 'closed':
                results['closed_ports'].append(port)
            else:
                results['filtered_ports'].append(port)
        
        return results
    
    def check_port(self, ip, port, timeout=1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            
            if result == 0:
                return 'open'
            else:
                return 'closed'
        except socket.error:
            return 'filtered'
    
    def check_udp_port(self, ip, port, timeout=1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout)
            sock.sendto(b'\x00', (ip, port))
            sock.close()
            return 'open|filtered'
        except Exception:
            return 'closed'
    
    def banner_entropy(self, banner):
        if not banner:
            return 0.0
        import math
        from collections import Counter
        counts = Counter(banner)
        total = sum(counts.values())
        return -sum((c/total) * math.log2(c/total) for c in counts.values())
    
    def identify_service(self, ip, port):
        service_map = {
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            143: 'IMAP',
            443: 'HTTPS',
            445: 'SMB',
            3306: 'MySQL',
            3389: 'RDP',
            5900: 'VNC',
            8080: 'HTTP-Alt',
            8443: 'HTTPS-Alt'
        }
        
        service = service_map.get(port, 'Unknown')
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((ip, port))
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            sock.close()
            
            return {
                'name': service,
                'banner': banner
            }
        except:
            return {
                'name': service,
                'banner': None
            }
    
    def enrich_service_info(self, ip, port, service_info):
        enriched = dict(service_info)
        enriched['entropy'] = self.banner_entropy(service_info.get('banner'))
        if port in (443, 8443, 9443):
            enriched['tls'] = self.capture_tls_certificate(ip, port)
        if port in (139, 445):
            enriched['smb_hint'] = 'SMB related port open'
        return enriched
    
    def capture_tls_certificate(self, host, port):
        try:
            import ssl
            context = ssl.create_default_context()
            with socket.create_connection((host, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()
                    return {
                        'subject': dict(x[0] for x in cert.get('subject', [])),
                        'issuer': dict(x[0] for x in cert.get('issuer', [])),
                        'not_after': cert.get('notAfter')
                    }
        except Exception as e:
            return {'error': str(e)}
    
    def enumerate_smb_netbios(self, ports_result):
        open_ports = [p['port'] for p in ports_result.get('open_ports', [])] if isinstance(ports_result, dict) else []
        return {'smb_present': any(p in (139, 445) for p in open_ports)}
    
    def reverse_dns_sweep(self, ip, limit=16):
        try:
            ip_addr = ipaddress.ip_address(ip)
            network = ipaddress.ip_network(f"{ip_addr}/24", strict=False)
            results = []
            for host in list(network.hosts())[:limit]:
                try:
                    name = socket.gethostbyaddr(str(host))[0]
                    results.append({'ip': str(host), 'hostname': name})
                except Exception:
                    continue
            return results
        except Exception as e:
            return {'error': str(e)}
    
    def snmp_public_check(self, ip):
        # Placeholder safe check
        return {'checked': False, 'note': 'SNMP check disabled by default'}
    
    def ssh_host_key_fingerprint(self, ip):
        return {'fingerprint': None, 'note': 'SSH key fingerprinting requires additional libraries'}
    
    def get_network_info(self, cidr):
        try:
            network = ipaddress.ip_network(cidr)
            return {
                'network': str(network.network_address),
                'netmask': str(network.netmask),
                'broadcast': str(network.broadcast_address),
                'num_addresses': network.num_addresses,
                'hosts': [str(ip) for ip in list(network.hosts())[:10]]
            }
        except Exception as e:
            return {'error': str(e)}
