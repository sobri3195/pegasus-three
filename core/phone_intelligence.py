"""
Phone Intelligence Module - Phone number analysis and lookup
"""

import re
import requests
from datetime import datetime
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

class PhoneIntelligence:
    def __init__(self, config):
        self.config = config
        
    def lookup(self, phone_number):
        results = {
            'phone_number': phone_number,
            'timestamp': datetime.now().isoformat(),
            'validation': self.validate_phone(phone_number),
            'carrier_info': self.get_carrier_info(phone_number),
            'location': self.get_location(phone_number),
            'timezone': self.get_timezone(phone_number),
            'format_info': self.get_format_info(phone_number),
            'regional_format_hint': self.regional_format_hint(phone_number),
            'ndc_analysis': self.analyze_ndc(phone_number),
            'contact_window': self.suggest_contact_window(phone_number),
            'cnam': self.cnam_lookup(phone_number),
            'reachability': self.reachability_category(phone_number),
            'country_risk': self.country_risk_map(phone_number),
            'risk_assessment': self.assess_risk(phone_number)
        }
        return results
    
    def validate_phone(self, phone_number):
        try:
            parsed = phonenumbers.parse(phone_number, None)
            
            return {
                'valid': phonenumbers.is_valid_number(parsed),
                'possible': phonenumbers.is_possible_number(parsed),
                'country_code': parsed.country_code,
                'national_number': parsed.national_number,
                'number_type': self.get_number_type(parsed)
            }
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
    
    def get_number_type(self, parsed_number):
        number_type = phonenumbers.number_type(parsed_number)
        types = {
            0: 'FIXED_LINE',
            1: 'MOBILE',
            2: 'FIXED_LINE_OR_MOBILE',
            3: 'TOLL_FREE',
            4: 'PREMIUM_RATE',
            5: 'SHARED_COST',
            6: 'VOIP',
            7: 'PERSONAL_NUMBER',
            8: 'PAGER',
            9: 'UAN',
            10: 'VOICEMAIL',
            27: 'UNKNOWN'
        }
        return types.get(number_type, 'UNKNOWN')
    
    def get_carrier_info(self, phone_number):
        try:
            parsed = phonenumbers.parse(phone_number, None)
            carrier_name = carrier.name_for_number(parsed, 'en')
            
            return {
                'carrier': carrier_name if carrier_name else 'Unknown',
                'network_type': self.get_number_type(parsed)
            }
        except Exception as e:
            return {
                'carrier': 'Unknown',
                'error': str(e)
            }
    
    def get_location(self, phone_number):
        try:
            parsed = phonenumbers.parse(phone_number, None)
            location = geocoder.description_for_number(parsed, 'en')
            
            return {
                'location': location if location else 'Unknown',
                'country_code': phonenumbers.region_code_for_number(parsed)
            }
        except Exception as e:
            return {
                'location': 'Unknown',
                'error': str(e)
            }
    
    def get_timezone(self, phone_number):
        try:
            parsed = phonenumbers.parse(phone_number, None)
            timezones = timezone.time_zones_for_number(parsed)
            
            return {
                'timezones': list(timezones) if timezones else []
            }
        except Exception as e:
            return {
                'timezones': [],
                'error': str(e)
            }
    
    def get_format_info(self, phone_number):
        try:
            parsed = phonenumbers.parse(phone_number, None)
            
            return {
                'international': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                'national': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
                'e164': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
                'rfc3966': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.RFC3966)
            }
        except Exception as e:
            return {
                'error': str(e)
            }
    
    def regional_format_hint(self, phone_number):
        try:
            parsed = phonenumbers.parse(phone_number, None)
            region = phonenumbers.region_code_for_number(parsed)
            national = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
            return {'region': region, 'hint': national}
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_ndc(self, phone_number):
        try:
            parsed = phonenumbers.parse(phone_number, None)
            ndc_length = phonenumbers.length_of_national_destination_code(parsed)
            ndc = phonenumbers.national_significant_number(parsed)[:ndc_length] if ndc_length else None
            return {'ndc': ndc, 'length': ndc_length}
        except Exception as e:
            return {'error': str(e)}
    
    def suggest_contact_window(self, phone_number):
        try:
            tz = self.get_timezone(phone_number).get('timezones', [])
            return {'timezones': tz, 'suggested_local_hours': '09:00-18:00'}
        except Exception as e:
            return {'error': str(e)}
    
    def cnam_lookup(self, phone_number):
        return {'available': False, 'note': 'CNAM lookup requires external API'}
    
    def reachability_category(self, phone_number):
        try:
            parsed = phonenumbers.parse(phone_number, None)
            t = self.get_number_type(parsed)
            category = 'likely' if t in ['MOBILE', 'FIXED_LINE', 'FIXED_LINE_OR_MOBILE'] else 'unknown'
            return {'category': category}
        except Exception as e:
            return {'category': 'unknown', 'error': str(e)}
    
    def country_risk_map(self, phone_number):
        try:
            parsed = phonenumbers.parse(phone_number, None)
            region = phonenumbers.region_code_for_number(parsed)
            high_risk = {'NG', 'RU'}
            medium_risk = {'CN', 'BR'}
            level = 'LOW'
            if region in high_risk:
                level = 'HIGH'
            elif region in medium_risk:
                level = 'MEDIUM'
            return {'country': region, 'risk_level': level}
        except Exception as e:
            return {'error': str(e)}
    
    def assess_risk(self, phone_number):
        risk_score = 0
        risk_factors = []
        
        try:
            parsed = phonenumbers.parse(phone_number, None)
            
            if not phonenumbers.is_valid_number(parsed):
                risk_score += 50
                risk_factors.append('Invalid number')
            
            number_type = self.get_number_type(parsed)
            if number_type in ['PREMIUM_RATE', 'SHARED_COST']:
                risk_score += 30
                risk_factors.append('Premium/Shared cost number')
            
            if number_type == 'VOIP':
                risk_score += 20
                risk_factors.append('VOIP number')
            
            carrier_info = self.get_carrier_info(phone_number)
            if carrier_info.get('carrier') == 'Unknown':
                risk_score += 10
                risk_factors.append('Unknown carrier')
            
            # Ported and virtual hints
            if number_type in ['VOIP']:
                risk_factors.append('Possible virtual/throwaway number')
            
        except Exception:
            risk_score = 100
            risk_factors.append('Parse error')
        
        risk_level = 'LOW'
        if risk_score > 70:
            risk_level = 'HIGH'
        elif risk_score > 40:
            risk_level = 'MEDIUM'
        
        return {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'risk_factors': risk_factors
        }
    
    def search_phone_number(self, phone_number):
        results = {
            'truecaller': self.search_truecaller(phone_number),
            'whitepages': self.search_whitepages(phone_number)
        }
        return results
    
    def search_truecaller(self, phone_number):
        return {
            'available': False,
            'message': 'API key required'
        }
    
    def search_whitepages(self, phone_number):
        return {
            'available': False,
            'message': 'API key required'
        }
    
    def generate_call_detail_record(self, phone_number, duration, timestamp):
        return {
            'phone_number': phone_number,
            'duration': duration,
            'timestamp': timestamp,
            'type': 'outgoing',
            'cost': 0.0
        }
