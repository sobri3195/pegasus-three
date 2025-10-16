# Contributing to Pegasus Three

Thank you for your interest in contributing to Pegasus Three OSINT Toolkit!

## Code of Conduct

### Our Standards

- Use welcoming and inclusive language
- Respect differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

### Ethical Requirements

All contributors must:
- Commit to ethical use of OSINT techniques
- Not contribute features designed for illegal activities
- Respect privacy and data protection laws
- Include appropriate warnings for sensitive features
- Follow responsible disclosure practices

## How to Contribute

### Reporting Bugs

1. Check existing issues first
2. Use the bug report template
3. Include:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information
   - Relevant logs

### Suggesting Features

1. Check existing feature requests
2. Explain the use case
3. Describe expected behavior
4. Consider legal and ethical implications
5. Provide examples if possible

### Pull Requests

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit PR with clear description

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/pegasus-three.git
cd pegasus-three

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy
```

### Coding Standards

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for all functions
- Keep functions focused and modular
- Add comments for complex logic

### Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=core tests/
```

### Documentation

- Update README.md for major changes
- Add docstrings to new functions
- Update USAGE.md for new features
- Include examples in documentation

## Legal Considerations

### What We Accept

✅ Features for gathering public information
✅ Improvements to existing modules
✅ Bug fixes and performance improvements
✅ Documentation improvements
✅ Better error handling
✅ Security enhancements

### What We Don't Accept

❌ Features for unauthorized access
❌ Tools for illegal surveillance
❌ Exploits or malware
❌ Features that violate privacy laws
❌ Anything promoting illegal activities

## Review Process

1. Maintainers review all PRs
2. Automated tests must pass
3. Code review and feedback
4. Approval from at least one maintainer
5. Merge when ready

## Questions?

Open an issue or contact maintainers.

Thank you for contributing responsibly!
