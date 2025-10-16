#!/bin/bash
# Pegasus Three - Quick Start Script

echo "=================================================="
echo "Pegasus Three OSINT Toolkit - Quick Start"
echo "=================================================="
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Python version: $PYTHON_VERSION"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo ""
echo "Installing dependencies..."
echo "(This may take a few minutes...)"
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "✓ Dependencies installed"

# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p reports logs
echo "✓ Directories created"

# Display legal notice
echo ""
echo "=================================================="
echo "⚠️  LEGAL NOTICE"
echo "=================================================="
echo "This tool is for AUTHORIZED USE ONLY."
echo ""
echo "You must:"
echo "• Have proper authorization for investigations"
echo "• Comply with all applicable laws"
echo "• Use only for legal and ethical purposes"
echo "• NOT use for harassment or stalking"
echo ""
echo "Unauthorized use may result in legal action."
echo "=================================================="
echo ""

# Display usage examples
echo "Quick Start Examples:"
echo ""
echo "1. Domain reconnaissance:"
echo "   python pegasus.py --domain example.com"
echo ""
echo "2. Username search:"
echo "   python pegasus.py --username johndoe --module social"
echo ""
echo "3. Email investigation:"
echo "   python pegasus.py --email test@example.com --module email"
echo ""
echo "4. Run example script:"
echo "   python examples/basic_scan.py"
echo ""
echo "5. Display help:"
echo "   python pegasus.py --help"
echo ""
echo "=================================================="
echo "For more information, see:"
echo "• README.md - Overview and features"
echo "• USAGE.md - Detailed usage guide"
echo "• SECURITY.md - Security best practices"
echo "=================================================="
echo ""
echo "Setup complete! You can now use Pegasus OSINT Toolkit."
echo ""
