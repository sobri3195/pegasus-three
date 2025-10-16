#!/usr/bin/env python3
"""
Basic functionality test for Pegasus OSINT Toolkit
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported"""
    print("Testing module imports...")
    
    try:
        from core.osint_module import OSINTModule
        print("✓ OSINT Module")
    except ImportError as e:
        print(f"✗ OSINT Module: {e}")
        return False
    
    try:
        from core.social_intelligence import SocialIntelligence
        print("✓ Social Intelligence Module")
    except ImportError as e:
        print(f"✗ Social Intelligence Module: {e}")
        return False
    
    try:
        from core.network_intelligence import NetworkIntelligence
        print("✓ Network Intelligence Module")
    except ImportError as e:
        print(f"✗ Network Intelligence Module: {e}")
        return False
    
    try:
        from core.email_intelligence import EmailIntelligence
        print("✓ Email Intelligence Module")
    except ImportError as e:
        print(f"✗ Email Intelligence Module: {e}")
        return False
    
    try:
        from core.phone_intelligence import PhoneIntelligence
        print("✓ Phone Intelligence Module")
    except ImportError as e:
        print(f"✗ Phone Intelligence Module: {e}")
        return False
    
    try:
        from core.metadata_extractor import MetadataExtractor
        print("✓ Metadata Extractor Module")
    except ImportError as e:
        print(f"✗ Metadata Extractor Module: {e}")
        return False
    
    try:
        from core.profiler import DataProfiler
        print("✓ Data Profiler Module")
    except ImportError as e:
        print(f"✗ Data Profiler Module: {e}")
        return False
    
    try:
        from core.report_generator import ReportGenerator
        print("✓ Report Generator Module")
    except ImportError as e:
        print(f"✗ Report Generator Module: {e}")
        return False
    
    try:
        from modules.doxing import DoxingModule
        print("✓ Doxing Module")
    except ImportError as e:
        print(f"✗ Doxing Module: {e}")
        return False
    
    try:
        from modules.tracking import TrackingModule
        print("✓ Tracking Module")
    except ImportError as e:
        print(f"✗ Tracking Module: {e}")
        return False
    
    try:
        from modules.spy import SurveillanceModule
        print("✓ Surveillance Module")
    except ImportError as e:
        print(f"✗ Surveillance Module: {e}")
        return False
    
    try:
        from utils.logger import setup_logger
        print("✓ Logger Utility")
    except ImportError as e:
        print(f"✗ Logger Utility: {e}")
        return False
    
    try:
        from utils.banner import print_banner
        print("✓ Banner Utility")
    except ImportError as e:
        print(f"✗ Banner Utility: {e}")
        return False
    
    try:
        from utils.validator import validate_inputs
        print("✓ Validator Utility")
    except ImportError as e:
        print(f"✗ Validator Utility: {e}")
        return False
    
    return True

def test_configuration():
    """Test configuration loading"""
    print("\nTesting configuration...")
    
    try:
        import json
        from pathlib import Path
        
        config_file = Path('config.json')
        if not config_file.exists():
            print("✗ config.json not found")
            return False
        
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        print("✓ Configuration file loaded")
        
        required_keys = ['api_keys', 'scan_intensity', 'output_format', 'timeout', 'user_agent']
        for key in required_keys:
            if key in config:
                print(f"  ✓ {key}")
            else:
                print(f"  ✗ Missing key: {key}")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_validators():
    """Test input validators"""
    print("\nTesting validators...")
    
    try:
        from utils.validator import validate_domain, validate_email, validate_ip, validate_phone
        
        # Test domain validation
        assert validate_domain('example.com') == True
        assert validate_domain('invalid domain') == False
        print("✓ Domain validator")
        
        # Test email validation
        assert validate_email('test@example.com') == True
        assert validate_email('invalid-email') == False
        print("✓ Email validator")
        
        # Test IP validation
        assert validate_ip('192.168.1.1') == True
        assert validate_ip('999.999.999.999') == False
        print("✓ IP validator")
        
        # Test phone validation
        assert validate_phone('+12345678900') == True
        print("✓ Phone validator")
        
        return True
    except Exception as e:
        print(f"✗ Validator test failed: {e}")
        return False

def test_module_initialization():
    """Test module initialization"""
    print("\nTesting module initialization...")
    
    config = {'user_agent': 'Test', 'timeout': 10}
    
    try:
        from core.osint_module import OSINTModule
        osint = OSINTModule(config)
        print("✓ OSINT Module initialized")
    except Exception as e:
        print(f"✗ OSINT Module: {e}")
        return False
    
    try:
        from core.social_intelligence import SocialIntelligence
        social = SocialIntelligence(config)
        print("✓ Social Intelligence initialized")
    except Exception as e:
        print(f"✗ Social Intelligence: {e}")
        return False
    
    try:
        from core.profiler import DataProfiler
        profiler = DataProfiler(config)
        print("✓ Data Profiler initialized")
    except Exception as e:
        print(f"✗ Data Profiler: {e}")
        return False
    
    return True

def main():
    print("="*60)
    print("Pegasus Three - Basic Functionality Tests")
    print("="*60)
    print()
    
    tests_passed = 0
    tests_failed = 0
    
    # Run tests
    if test_imports():
        tests_passed += 1
    else:
        tests_failed += 1
    
    if test_configuration():
        tests_passed += 1
    else:
        tests_failed += 1
    
    if test_validators():
        tests_passed += 1
    else:
        tests_failed += 1
    
    if test_module_initialization():
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    print(f"Tests passed: {tests_passed}")
    print(f"Tests failed: {tests_failed}")
    print("="*60)
    
    if tests_failed == 0:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {tests_failed} test(s) failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
