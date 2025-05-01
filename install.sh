#!/bin/bash

# Laser Optics Diagram Tool - Installation Script
# This script helps set up the project environment

echo "Setting up Laser Optics Diagram Tool..."

# Create build directory structure if it doesn't exist
mkdir -p build/schematics build/tests build/docs build/cheatsheets
echo "✓ Created build directories"

# Make Python script executable
chmod +x src/optical_diagram_creator.py
echo "✓ Made optical_diagram_creator.py executable"

# Check if xelatex is installed
if command -v xelatex &> /dev/null; then
    echo "✓ XeLaTeX is installed"
else
    echo "⚠ XeLaTeX not found. Please install TeX Live or another LaTeX distribution with XeLaTeX."
fi

# Check for required LaTeX packages
echo "Checking for required LaTeX packages..."
if xelatex -output-directory=/tmp -jobname=check_pkg \\
    <(echo '\\documentclass{article}\\usepackage{pst-optexp}\\begin{document}Test\\end{document}') &> /dev/null; then
    echo "✓ Required LaTeX packages are installed"
else
    echo "⚠ Some LaTeX packages may be missing. Please ensure pstricks and pst-optexp are installed."
fi

# Check for Python and tkinter
if command -v python3 &> /dev/null; then
    echo "✓ Python 3 is installed"
    
    # Try to import tkinter
    if python3 -c "import tkinter" &> /dev/null; then
        echo "✓ Tkinter is installed"
    else
        echo "⚠ Tkinter not found. Please install Tkinter for your Python distribution."
    fi
else
    echo "⚠ Python 3 not found. Please install Python 3 to use the GUI tool."
fi

echo ""
echo "Installation complete! You can now use the Laser Optics Diagram Tool."
echo ""
echo "Quick start:"
echo "  1. Run a simple test:        make test"
echo "  2. Launch the GUI:           ./src/optical_diagram_creator.py"
echo "  3. Build a custom diagram:   make build/schematics/your_file.pdf"
echo ""
echo "See README.md for more information." 