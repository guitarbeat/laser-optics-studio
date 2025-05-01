# Laser Optics Schematic Project

This repository contains LaTeX files for creating optical schematic diagrams using PSTricks and the pst-optexp package.

## Project Structure

```
.
├── src/                # Main source directory
│   ├── schematics/     # Schematic diagrams
│   ├── tests/          # Test files
│   ├── docs/           # Documentation
│   ├── templates/      # Template files
│   └── cheatsheets/    # Reference cheatsheets
└── build/              # Output directory (created by make)
    ├── schematics/     # Built schematic PDFs
    ├── tests/          # Built test PDFs
    ├── docs/           # Built documentation PDFs
    └── cheatsheets/    # Built cheatsheet PDFs
```

## Prerequisites

- LaTeX distribution (TeXLive or MikTeX recommended)
- PSTricks packages
- pst-optexp package for optical schematics

## Usage

### Building Files

```bash
# Build default example (imaging system schematic)
make

# Build all PDFs
make all-pdfs

# Build specific categories
make schematics
make tests
make docs
make cheatsheets

# Clean build artifacts
make clean
```

### Adding New Files

To add new files, place them in the appropriate directory under `src/`:

- For schematics: `src/schematics/`
- For tests: `src/tests/`
- For documentation: `src/docs/`
- For cheatsheets: `src/cheatsheets/`

Use the template in `src/templates/schematic_template.tex` as a starting point for new schematics.

## Imaging System Schematic

The primary schematic in this project is an optical imaging system that demonstrates:

- A light source
- Focusing optics
- Imaging lenses
- Detection setup

## License

This project is licensed under the MIT License - see the LICENSE file for details. 