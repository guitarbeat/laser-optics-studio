# Imaging System Documentation

This directory contains documentation for the optical imaging system schematics.

## System Overview

The imaging system is designed to demonstrate optical principles in a laser-based setup. Key components include:

- **Light Source**: A 1064 nm laser that provides the initial beam
- **Beam Expander**: Expands the beam to the desired diameter
- **Focusing Optics**: Controls the beam focus and shape
- **Imaging Lenses**: Creates the desired image magnification and quality
- **Detection System**: Collects the final image or measurement

## Schematic Files

- `imaging_system_schematic.tex` - The primary schematic showing the complete system

## Usage Notes

- The schematic is designed to be clear and modifiable
- Components can be adjusted by modifying their parameters in the LaTeX file
- Colors, dimensions, and labels can be customized as needed

## Building Documentation

```bash
# Build all documentation PDFs
make docs

# Build a specific documentation file
make build/docs/specific_file.pdf
``` 