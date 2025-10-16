# Pegasus Three - Usage Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Basic Operations](#basic-operations)
3. [Advanced Features](#advanced-features)
4. [API Reference](#api-reference)
5. [Legal and Ethical Guidelines](#legal-and-ethical-guidelines)

## Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/sobri3195/pegasus-three.git
cd pegasus-three

# Install dependencies
pip install -r requirements.txt

# Configure API keys (optional)
cp config.json config_local.json
# Edit config_local.json with your API keys
```

### Quick Start

```bash
# Display help
python pegasus.py --help

# Basic domain scan
python pegasus.py --domain example.com

# Social media username search
python pegasus.py --username johndoe --module social

# Email investigation
python pegasus.py --email user@example.com --module email
```

## Basic Operations

### Domain and IP Reconnaissance

```bash
# WHOIS lookup and DNS enumeration
python pegasus.py --domain example.com --module osint

# Deep scan with subdomain discovery
python pegasus.py --domain example.com --deep-scan

# IP address investigation
python pegasus.py --ip 8.8.8.8 --module network
```

### Social Media Intelligence

```bash
# Search username across platforms
python pegasus.py --username johndoe --module social

# Save results to file
python pegasus.py --username johndoe --module social --output report.html
```

### Email Intelligence

```bash
# Validate and investigate email
python pegasus.py --email test@example.com --module email

# Check for data breaches (requires API key)
python pegasus.py --email test@example.com --module email --format json
```

### Phone Number Lookup

```bash
# Analyze phone number
python pegasus.py --phone +12345678900 --module phone

# Get carrier and location information
python pegasus.py --phone +12345678900 --module phone --output phone_report.html
```

### Metadata Extraction

```bash
# Extract metadata from image
python pegasus.py --file /path/to/image.jpg --module metadata

# Extract GPS coordinates from photos
python pegasus.py --file photo.jpg --module metadata --format json
```

## Advanced Features

### Comprehensive Profiling

```bash
# Create complete profile from multiple sources
python pegasus.py \
    --target "John Doe" \
    --username johndoe \
    --email john@example.com \
    --phone +12345678900 \
    --profile \
    --output complete_profile.html
```

### Network Scanning

```bash
# Scan network with port detection
python pegasus.py --ip 192.168.1.1 --scan-ports --module network

# Service detection on specific IP
python pegasus.py --ip 10.0.0.1 --scan-ports --deep-scan
```

### Batch Processing

```python
from core.osint_module import OSINTModule
from core.profiler import DataProfiler

config = {...}
osint = OSINTModule(config)

# Process multiple domains
domains = ['example1.com', 'example2.com', 'example3.com']
for domain in domains:
    results = osint.scan(domain)
    print(f"Results for {domain}:", results)
```

### Report Generation

```bash
# Generate HTML report
python pegasus.py --domain example.com --output report.html --format html

# Generate PDF report (requires reportlab)
python pegasus.py --domain example.com --output report.pdf --format pdf

# Generate JSON for programmatic use
python pegasus.py --domain example.com --output report.json --format json
```

## API Reference

### Python API Usage

```python
from pegasus import PegasusOSINT

# Initialize
pegasus = PegasusOSINT()

# Run OSINT scan
results = pegasus.run_osint_scan('example.com')

# Social intelligence
social_data = pegasus.run_social_intelligence('username')

# Email investigation
email_data = pegasus.run_email_intelligence('email@example.com')

# Generate report
pegasus.generate_report('output.html', format='html')
```

### Module Integration

```python
from core.email_intelligence import EmailIntelligence
from core.phone_intelligence import PhoneIntelligence

config = {'api_keys': {}, 'timeout': 30}

# Email module
email_intel = EmailIntelligence(config)
results = email_intel.investigate('test@example.com')

# Phone module
phone_intel = PhoneIntelligence(config)
results = phone_intel.lookup('+12345678900')
```

## Configuration

### API Keys

Edit `config.json` to add your API keys:

```json
{
  "api_keys": {
    "shodan": "YOUR_SHODAN_KEY",
    "virustotal": "YOUR_VT_KEY",
    "haveibeenpwned": "YOUR_HIBP_KEY"
  }
}
```

### Proxy Configuration

```json
{
  "use_proxy": true,
  "proxy": {
    "http": "http://proxy:8080",
    "https": "https://proxy:8080"
  }
}
```

### Rate Limiting

```json
{
  "rate_limit": {
    "enabled": true,
    "requests_per_second": 5
  }
}
```

## Legal and Ethical Guidelines

### ⚠️ IMPORTANT LEGAL NOTICE

1. **Authorization Required**: Always obtain proper authorization before conducting investigations
2. **Privacy Laws**: Comply with GDPR, CCPA, and other privacy regulations
3. **Terms of Service**: Respect website terms of service and robots.txt
4. **Data Protection**: Securely store and handle any collected information
5. **Responsible Use**: Never use for harassment, stalking, or malicious purposes

### Ethical OSINT Practices

- Only gather publicly available information
- Respect privacy and data protection laws
- Obtain consent when required
- Use information responsibly
- Document your authorization
- Follow your organization's policies

### Prohibited Uses

- Unauthorized surveillance
- Stalking or harassment
- Identity theft
- Fraud or scams
- Violating privacy laws
- Unauthorized access to systems

## Troubleshooting

### Common Issues

**ImportError: No module named 'X'**
```bash
pip install -r requirements.txt
```

**API rate limit exceeded**
- Add delays between requests
- Use API keys for higher limits
- Enable rate limiting in config

**No results returned**
- Check internet connection
- Verify target format
- Check API key validity
- Review logs for errors

### Getting Help

- Check logs in `logs/` directory
- Use verbose mode: `python pegasus.py --verbose ...`
- Open an issue on GitHub
- Review documentation

## Best Practices

1. **Start Small**: Begin with basic scans before complex operations
2. **Use API Keys**: Get better results with proper API access
3. **Rate Limiting**: Respect rate limits to avoid blocks
4. **Data Storage**: Securely store collected intelligence
5. **Regular Updates**: Keep dependencies updated
6. **Legal Compliance**: Always verify legal authorization

## Examples

See the `examples/` directory for more usage examples and scripts.

## Support

For questions, issues, or contributions:
- GitHub Issues: https://github.com/sobri3195/pegasus-three/issues
- Documentation: https://github.com/sobri3195/pegasus-three/wiki
