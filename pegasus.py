#!/usr/bin/env python3
"""
Pegasus Three - OSINT Toolkit
Main entry point for the application
"""

import argparse
import sys
import json
from datetime import datetime
from pathlib import Path

from core.osint_module import OSINTModule
from core.social_intelligence import SocialIntelligence
from core.network_intelligence import NetworkIntelligence
from core.metadata_extractor import MetadataExtractor
from core.email_intelligence import EmailIntelligence
from core.phone_intelligence import PhoneIntelligence
from core.profiler import DataProfiler
from core.report_generator import ReportGenerator
from utils.logger import setup_logger
from utils.banner import print_banner
from utils.validator import validate_inputs

logger = setup_logger()

class PegasusOSINT:
    def __init__(self):
        self.config = self.load_config()
        self.results = {}
        
    def load_config(self):
        config_file = Path('config.json')
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        return self.get_default_config()
    
    def get_default_config(self):
        return {
            'api_keys': {},
            'scan_intensity': 'medium',
            'output_format': 'html',
            'use_proxy': False,
            'timeout': 30,
            'user_agent': 'Pegasus-OSINT/1.0'
        }
    
    def run_osint_scan(self, target):
        logger.info(f"Running OSINT scan on: {target}")
        osint = OSINTModule(self.config)
        self.results['osint'] = osint.scan(target)
        return self.results['osint']
    
    def run_social_intelligence(self, username):
        logger.info(f"Running social intelligence on username: {username}")
        social = SocialIntelligence(self.config)
        self.results['social'] = social.search_username(username)
        return self.results['social']
    
    def run_network_intelligence(self, target_ip, scan_ports=False):
        logger.info(f"Running network intelligence on: {target_ip}")
        network = NetworkIntelligence(self.config)
        self.results['network'] = network.scan(target_ip, scan_ports)
        return self.results['network']
    
    def run_metadata_extraction(self, file_path):
        logger.info(f"Extracting metadata from: {file_path}")
        extractor = MetadataExtractor(self.config)
        self.results['metadata'] = extractor.extract(file_path)
        return self.results['metadata']
    
    def run_email_intelligence(self, email):
        logger.info(f"Running email intelligence on: {email}")
        email_intel = EmailIntelligence(self.config)
        self.results['email'] = email_intel.investigate(email)
        return self.results['email']
    
    def run_phone_intelligence(self, phone):
        logger.info(f"Running phone intelligence on: {phone}")
        phone_intel = PhoneIntelligence(self.config)
        self.results['phone'] = phone_intel.lookup(phone)
        return self.results['phone']
    
    def create_profile(self, target_info):
        logger.info("Creating comprehensive profile")
        profiler = DataProfiler(self.config)
        self.results['profile'] = profiler.create_profile(self.results)
        return self.results['profile']
    
    def generate_report(self, output_file, format='html'):
        logger.info(f"Generating report: {output_file}")
        generator = ReportGenerator(self.config)
        return generator.generate(self.results, output_file, format)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Pegasus Three - OSINT Toolkit',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pegasus.py --domain example.com
  python pegasus.py --username johndoe --module social
  python pegasus.py --email test@example.com --module email
  python pegasus.py --target "John Doe" --profile --output report.html
        """
    )
    
    parser.add_argument('--domain', help='Target domain for OSINT')
    parser.add_argument('--ip', help='Target IP address')
    parser.add_argument('--username', help='Username to search')
    parser.add_argument('--email', help='Email address to investigate')
    parser.add_argument('--phone', help='Phone number to lookup')
    parser.add_argument('--file', help='File for metadata extraction')
    parser.add_argument('--target', help='General target identifier')
    
    parser.add_argument('--module', choices=['osint', 'social', 'network', 'email', 'phone', 'metadata'],
                       help='Specific module to run')
    parser.add_argument('--profile', action='store_true', help='Create comprehensive profile')
    parser.add_argument('--scan-ports', action='store_true', help='Enable port scanning')
    parser.add_argument('--deep-scan', action='store_true', help='Enable deep scanning')
    
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--format', choices=['html', 'json', 'pdf'], default='html',
                       help='Output format')
    parser.add_argument('--config', help='Custom config file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    return parser.parse_args()

def main():
    print_banner()
    
    args = parse_arguments()
    
    if not any([args.domain, args.ip, args.username, args.email, args.phone, args.file, args.target]):
        print("Error: Please specify at least one target parameter")
        print("Use --help for usage information")
        sys.exit(1)
    
    pegasus = PegasusOSINT()
    
    try:
        if args.domain or (args.target and not args.module):
            target = args.domain or args.target
            pegasus.run_osint_scan(target)
        
        if args.username or args.module == 'social':
            username = args.username or args.target
            pegasus.run_social_intelligence(username)
        
        if args.ip or args.module == 'network':
            ip = args.ip or args.target
            pegasus.run_network_intelligence(ip, args.scan_ports)
        
        if args.email or args.module == 'email':
            email = args.email or args.target
            pegasus.run_email_intelligence(email)
        
        if args.phone or args.module == 'phone':
            phone = args.phone or args.target
            pegasus.run_phone_intelligence(phone)
        
        if args.file or args.module == 'metadata':
            file_path = args.file or args.target
            pegasus.run_metadata_extraction(file_path)
        
        if args.profile:
            pegasus.create_profile(args.target)
        
        if args.output:
            pegasus.generate_report(args.output, args.format)
        else:
            print("\n" + "="*60)
            print("RESULTS")
            print("="*60)
            print(json.dumps(pegasus.results, indent=2))
        
        logger.info("Scan completed successfully")
        
    except KeyboardInterrupt:
        print("\n\n[!] Scan interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error during execution: {str(e)}")
        if args.verbose:
            raise
        sys.exit(1)

if __name__ == '__main__':
    main()
