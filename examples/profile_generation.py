#!/usr/bin/env python3
"""
Profile Generation Example
Demonstrates how to create comprehensive profiles
"""

import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.profiler import DataProfiler
from pegasus import PegasusOSINT

def main():
    print("="*60)
    print("Pegasus OSINT - Profile Generation Example")
    print("="*60)
    
    pegasus = PegasusOSINT()
    
    print("\n[*] Gathering information from multiple sources...")
    
    print("\n  [1/3] Domain reconnaissance...")
    try:
        pegasus.run_osint_scan('example.com')
        print("  ✓ Domain data collected")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    print("\n  [2/3] Social media intelligence...")
    try:
        pegasus.run_social_intelligence('example_user')
        print("  ✓ Social media data collected")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    print("\n  [3/3] Email investigation...")
    try:
        pegasus.run_email_intelligence('user@example.com')
        print("  ✓ Email data collected")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    print("\n[*] Creating comprehensive profile...")
    try:
        profile = pegasus.create_profile({'target': 'example_user'})
        print("✓ Profile created successfully")
        
        print("\n" + "-"*60)
        print("PROFILE SUMMARY")
        print("-"*60)
        
        summary = profile.get('summary', {})
        print(f"Data Sources: {summary.get('total_sources', 0)}")
        print(f"Confidence Score: {summary.get('confidence_score', 0)}%")
        print(f"Data Quality: {summary.get('data_quality', {}).get('score', 0)}%")
        
        identity = profile.get('identity', {})
        print(f"\nUsernames: {', '.join(identity.get('usernames', []))}")
        print(f"Emails: {', '.join(identity.get('emails', []))}")
        
        risk = profile.get('risk_assessment', {})
        print(f"\nRisk Level: {risk.get('risk_level', 'UNKNOWN')}")
        print(f"Risk Score: {risk.get('risk_score', 0)}/100")
        
    except Exception as e:
        print(f"✗ Error creating profile: {e}")
    
    print("\n[*] Generating comprehensive report...")
    try:
        os.makedirs('reports', exist_ok=True)
        pegasus.generate_report('reports/profile_report.html', 'html')
        print("✓ HTML report: reports/profile_report.html")
        
        pegasus.generate_report('reports/profile_data.json', 'json')
        print("✓ JSON data: reports/profile_data.json")
    except Exception as e:
        print(f"✗ Error generating report: {e}")
    
    print("\n" + "="*60)
    print("Profile generation completed!")
    print("="*60)

if __name__ == '__main__':
    main()
