"""
Input validation utility for Pegasus OSINT
"""

import re
import ipaddress

def validate_inputs(args):
    errors = []
    
    if args.get('domain'):
        if not validate_domain(args['domain']):
            errors.append(f"Invalid domain: {args['domain']}")
    
    if args.get('ip'):
        if not validate_ip(args['ip']):
            errors.append(f"Invalid IP address: {args['ip']}")
    
    if args.get('email'):
        if not validate_email(args['email']):
            errors.append(f"Invalid email: {args['email']}")
    
    if args.get('phone'):
        if not validate_phone(args['phone']):
            errors.append(f"Invalid phone number: {args['phone']}")
    
    return errors

def validate_domain(domain):
    pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    return bool(re.match(pattern, domain))

def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone):
    pattern = r'^\+?[1-9]\d{1,14}$'
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    return bool(re.match(pattern, cleaned))

def sanitize_input(input_string):
    dangerous_chars = ['<', '>', '&', '"', "'", ';', '|', '`']
    for char in dangerous_chars:
        input_string = input_string.replace(char, '')
    return input_string

def validate_file_path(file_path):
    import os
    return os.path.exists(file_path) and os.path.isfile(file_path)
