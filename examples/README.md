# Pegasus Three - Examples

This directory contains example scripts demonstrating various features of the Pegasus OSINT toolkit.

## Available Examples

### 1. basic_scan.py
Basic usage example showing fundamental OSINT operations.

**Features demonstrated:**
- Domain reconnaissance
- Social media username search
- Report generation

**Usage:**
```bash
python examples/basic_scan.py
```

### 2. profile_generation.py
Comprehensive profile creation from multiple sources.

**Features demonstrated:**
- Multi-source data collection
- Profile aggregation
- Risk assessment
- Multiple report formats

**Usage:**
```bash
python examples/profile_generation.py
```

### 3. tracking_demo.py
Tracking and monitoring capabilities demonstration.

**Features demonstrated:**
- Baseline creation
- Change detection
- Alert configuration
- Tracking profile management

**Usage:**
```bash
python examples/tracking_demo.py
```

## Creating Your Own Scripts

### Basic Template

```python
#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pegasus import PegasusOSINT

def main():
    # Initialize
    pegasus = PegasusOSINT()
    
    # Run your investigation
    results = pegasus.run_osint_scan('example.com')
    
    # Generate report
    pegasus.generate_report('output.html', 'html')

if __name__ == '__main__':
    main()
```

### Custom Module Usage

```python
#!/usr/bin/env python3
from core.email_intelligence import EmailIntelligence

config = {'timeout': 30, 'user_agent': 'Custom-Agent'}
email_intel = EmailIntelligence(config)

results = email_intel.investigate('test@example.com')
print(results)
```

## Tips

1. **Always check authorization** before running investigations
2. **Use verbose mode** for debugging: add `--verbose` flag
3. **Start with basic scans** before comprehensive profiles
4. **Save outputs** for later analysis
5. **Review logs** in the `logs/` directory

## Legal Notice

All examples are for **educational and authorized use only**. Always ensure you have proper authorization before conducting any investigation.

## Need Help?

- Check the main documentation: `../USAGE.md`
- Review security guidelines: `../SECURITY.md`
- Open an issue on GitHub
