#!/usr/bin/env python3
"""
Basic OSINT Scan Example
Demonstrates basic usage of Pegasus OSINT toolkit
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pegasus import PegasusOSINT
from utils.logger import setup_logger

logger = setup_logger()

def main():
    print("="*60)
    print("Pegasus OSINT - Basic Scan Example")
    print("="*60)
    
    pegasus = PegasusOSINT()
    
    print("\n[1] Running OSINT scan on example.com...")
    try:
        results = pegasus.run_osint_scan('example.com')
        print("✓ OSINT scan completed")
        print(f"  - Domain: {results.get('target')}")
        print(f"  - IP: {results.get('ip_info', {}).get('ip_address')}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n[2] Searching username 'johndoe' across platforms...")
    try:
        social_results = pegasus.run_social_intelligence('johndoe')
        print("✓ Social intelligence scan completed")
        print(f"  - Platforms found: {len(social_results.get('platforms_found', []))}")
        print(f"  - Platforms: {', '.join(social_results.get('platforms_found', []))}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n[3] Generating report...")
    try:
        report_file = 'reports/basic_scan_report.html'
        os.makedirs('reports', exist_ok=True)
        pegasus.generate_report(report_file, 'html')
        print(f"✓ Report generated: {report_file}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "="*60)
    print("Scan completed!")
    print("="*60)

if __name__ == '__main__':
    main()
