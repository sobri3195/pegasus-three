#!/usr/bin/env python3
"""
Tracking Module Demo
Demonstrates tracking and monitoring capabilities
WARNING: For authorized use only
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.tracking import TrackingModule
from pegasus import PegasusOSINT
import json

def main():
    print("="*60)
    print("Pegasus OSINT - Tracking Module Demo")
    print("="*60)
    
    print("\n⚠️  LEGAL WARNING")
    print("This demo is for educational purposes only.")
    print("Ensure you have proper authorization before tracking.")
    print("="*60)
    
    config = {'user_agent': 'Pegasus-OSINT/1.0'}
    tracking = TrackingModule(config)
    
    print("\n[1] Gathering initial baseline data...")
    pegasus = PegasusOSINT()
    
    try:
        osint_data = pegasus.run_osint_scan('example.com')
        social_data = pegasus.run_social_intelligence('testuser')
        
        collected_data = {
            'osint': osint_data,
            'social': social_data
        }
        
        print("✓ Baseline data collected")
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    print("\n[2] Creating tracking profile...")
    try:
        profile = tracking.create_tracking_profile('target_001', collected_data)
        print("✓ Tracking profile created")
        print(f"  - Target ID: {profile['target_id']}")
        print(f"  - Monitoring points: {len(profile['monitoring_points'])}")
        print(f"  - Alert rules: {len(profile['alert_rules'])}")
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    print("\n[3] Identifying monitoring points...")
    for point in profile['monitoring_points']:
        print(f"  • {point['type']}: {point.get('platform', point.get('target', 'N/A'))}")
        print(f"    Check interval: {point['check_interval']}s")
    
    print("\n[4] Active alert rules...")
    for rule in profile['alert_rules']:
        if rule['enabled']:
            print(f"  • [{rule['severity'].upper()}] {rule['description']}")
    
    print("\n[5] Creating baseline snapshot...")
    baseline = tracking.create_baseline(collected_data)
    print("✓ Baseline snapshot created")
    print(f"  - Social platforms: {baseline['social_presence'].get('profile_count', 0)}")
    print(f"  - Domain: {baseline['domain_status'].get('domain', 'N/A')}")
    
    print("\n[6] Simulating comparison (no changes)...")
    changes = tracking.compare_snapshots(baseline, baseline)
    print(f"✓ Comparison completed")
    print(f"  - Changes detected: {changes['change_count']}")
    print(f"  - Severity: {changes['severity']}")
    
    print("\n[7] Setting up alerts...")
    geofence = tracking.create_geofence_alert('target_001', {'lat': 0, 'lon': 0}, 1000)
    print(f"✓ Geofence alert created: {geofence['alert_id']}")
    
    keyword_alert = tracking.create_keyword_alert('target_001', ['suspicious', 'urgent'])
    print(f"✓ Keyword alert created: {keyword_alert['alert_id']}")
    
    print("\n[8] Exporting tracking report...")
    try:
        report = tracking.export_tracking_report('target_001', time_range='last_24h')
        report_file = 'reports/tracking_report.json'
        os.makedirs('reports', exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✓ Report exported: {report_file}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "="*60)
    print("Tracking demo completed!")
    print("Remember: Use responsibly and legally only.")
    print("="*60)

if __name__ == '__main__':
    main()
