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
        
        return results
    
    def get_host_info(self, ip):
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return {
                'ip': ip,
                'hostname': hostname,
                'is_valid': self.validate_ip(ip)
            }
        except Exception as e:
            return {
                'ip': ip,
                'hostname': None,
                'error': str(e),
                'is_valid': self.validate_ip(ip)
            }
    
    def validate_ip(self, ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    def ping_host(self, target):
        try:
            param = '-n' if subprocess.os.name == 'nt' else '-c'
            command = ['ping', param, '4', target]
            output = subprocess.run(command, capture_output=True, text=True, timeout=10)
            
            return {
                'success': output.returncode == 0,
                'output': output.stdout,
                'response_time': self.parse_ping_time(output.stdout)
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
    
    def traceroute(self, target):
        try:
            command = ['traceroute', target] if subprocess.os.name != 'nt' else ['tracert', target]
            output = subprocess.run(command, capture_output=True, text=True, timeout=30)
            
            return {
                'success': output.returncode == 0,
                'hops': self.parse_traceroute(output.stdout)
            }
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
                results['open_ports'].append({
                    'port': port,
                    'service': service
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
