# Laser Optics Diagram Tool

A specialized tool for creating professional-quality optical diagrams for laser setups and scientific publications. This project provides multiple ways to create diagrams:

1. **LaTeX with pst-optexp**: Direct use of LaTeX with the pst-optexp package
2. **Python GUI Interface**: A user-friendly graphical interface for creating diagrams without writing LaTeX code
3. **Custom AI Agent**: A specialized Cursor AI agent for optical diagram creation

## Features

- Create complex optical diagrams with exact positioning of components
- Professional-quality output suitable for publications and presentations
- Component library with common optical elements (mirrors, lenses, beam splitters, etc.)
- Color-coded beam paths to represent different wavelengths
- Export to PDF, SVG, or other formats

## Project Structure

```
lasers/
├── build/                    # Output directory for compiled diagrams
├── src/                      # Source files
│   ├── cheatsheets/          # Quick reference examples
│   ├── docs/                 # Documentation
│   ├── schematics/           # Schematic diagrams
│   ├── templates/            # Reusable templates
│   └── tests/                # Test files
│   └── optical_diagram_creator.py  # Python GUI tool
├── xnotes/                   # Project notes and configuration
├── Makefile                  # Build automation
└── README.md                 # Project documentation
```

## Getting Started

### Prerequisites

- LaTeX installation with PSTricks and pst-optexp packages
- Python 3.6+ with Tkinter (for the GUI interface)
- XeLaTeX (recommended for PDF generation)

### Building Diagrams with LaTeX

1. Create a new .tex file in the `src/schematics/` directory (see templates for examples)
2. Use the Makefile to build your diagram:

```bash
# Build a specific schematic
make build/schematics/your_file.pdf

# Build all schematics
make schematics

# Build a simple example to test the system
make test
```

### Using the Python GUI

1. Run the Python GUI tool:

```bash
python src/optical_diagram_creator.py
```

2. Use the component library to add optical elements to your diagram
3. Configure component properties as needed
4. Generate LaTeX code or export directly to PDF

### Using the Custom AI Agent

This project includes a custom Cursor AI agent specialized in optical diagrams. To use it:

1. Open the project in Cursor AI
2. Create a custom agent using the prompt in `xnotes/custom-agents.md`
3. Describe your optical setup to the agent in natural language
4. The agent will help create the LaTeX code and generate the diagram

## Examples

See the `src/cheatsheets/` directory for simple examples and the `src/schematics/` directory for more complex diagrams.

## Contributing

Contributions welcome! Add to the component library, improve the GUI, or enhance the LaTeX templates.

## License

MIT License 