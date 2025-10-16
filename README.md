# Pegasus Three - OSINT Toolkit

A comprehensive Open Source Intelligence (OSINT) framework for information gathering, profiling, and reconnaissance from publicly available sources.

## ⚠️ Legal Disclaimer

This tool is designed for **LEGAL AND ETHICAL USE ONLY**. Users must comply with all applicable laws and regulations. This includes:

- Obtaining proper authorization before conducting investigations
- Respecting privacy laws and regulations (GDPR, CCPA, etc.)
- Using gathered information responsibly and ethically
- NOT using this tool for harassment, stalking, or malicious purposes

**The developers assume no liability for misuse of this software.**

## Features

### 🔍 Core Modules

1. **OSINT Module** - Open source intelligence gathering
   - Domain/IP reconnaissance
   - WHOIS lookups
   - DNS enumeration
   - Subdomain discovery
   
2. **Social Media Intelligence** - Public profile analysis
   - Username search across platforms
   - Profile information gathering
   - Public post analysis
   
3. **Network Intelligence** - Network reconnaissance
   - Port scanning
   - Service detection
   - Network mapping
   
4. **Metadata Extraction** - File analysis
   - EXIF data extraction
   - Document metadata
   - Geolocation from images
   
5. **Email Intelligence** - Email investigation
   - Email validation
   - Breach database checks
   - Email format patterns
   
6. **Phone Intelligence** - Phone number analysis
   - Carrier lookup
   - Location information
   - Number validation
   
7. **Data Profiling** - Information aggregation
   - Profile building from multiple sources
   - Timeline creation
   - Relationship mapping
   
8. **Report Generation** - Documentation
   - HTML reports
   - PDF exports
   - JSON data dumps

## Installation

```bash
# Clone the repository
git clone https://github.com/sobri3195/pegasus-three.git
cd pegasus-three

# Install dependencies
pip install -r requirements.txt

# Run setup
python setup.py install
```

## Quick Start

```bash
# Basic OSINT scan
python pegasus.py --target example.com --module osint

# Social media username search
python pegasus.py --username johndoe --module social

# Phone number lookup
python pegasus.py --phone +1234567890 --module phone

# Email investigation
python pegasus.py --email target@example.com --module email

# Full profile generation
python pegasus.py --target "John Doe" --profile --output report.html
```

## Usage Examples

### Domain Investigation
```bash
python pegasus.py --domain example.com --deep-scan
```

### Multi-source Profiling
```bash
python pegasus.py --target "John Doe" --username johndoe --email john@example.com --profile
```

### Network Reconnaissance
```bash
python pegasus.py --ip 192.168.1.1 --scan-ports --service-detection
```

## Configuration

Edit `config.json` to customize:
- API keys for various services
- Scan intensity levels
- Output formats
- Proxy settings

## Requirements

- Python 3.8+
- Internet connection
- API keys for enhanced features (optional)

## Ethical Guidelines

1. **Authorization**: Always obtain proper authorization before investigating
2. **Privacy**: Respect individuals' privacy rights
3. **Legality**: Ensure compliance with local laws
4. **Responsibility**: Use information gathered responsibly
5. **Transparency**: Be transparent about your intentions when possible

## Contributing

Contributions are welcome! Please read CONTRIBUTING.md for guidelines.

## License

MIT License - See LICENSE file for details

## Support

For issues and questions, please open a GitHub issue.
