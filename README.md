# Laser Optics Diagram Tool

A graphical interface for creating optical diagrams using the pst-optexp LaTeX package. This tool allows drag-and-drop placement of optical components, configuration of their properties, and automatic generation of LaTeX code with PDF output.

## Features

- Graphical component library with common optical elements:
  - **Light Sources**: Lasers, LEDs
  - **Optical Components**: Lenses, mirrors, beam splitters, wave plates
  - **Detectors**: Photodiodes, cameras
- Interactive canvas for designing optical setups
- Automatic LaTeX code generation
- Direct PDF export capability
- Built-in LaTeX preview

## System Requirements

- Python 3
- Tkinter (for GUI)
- LaTeX distribution with pst-optexp package

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run the application with:

```bash
python3 src/main.py
```

## Documentation

- Component reference: `docs/component-reference.md`
- Docs index: `docs/README.md`

## Project Structure

The project follows a modular architecture:

```
src/
├── app/                  # Main application code
│   ├── gui/              # GUI components
│   │   ├── application.py     # Main application class
│   │   ├── canvas_manager.py  # Canvas drawing and interaction
│   │   └── component_library.py # Component library management
│   ├── models/           # Data models
│   │   ├── diagram.py         # Diagram model
│   │   └── optical_component.py # Component models
│   └── utils/            # Utility functions
│       ├── export.py          # PDF and other exports
│       └── latex_generator.py # LaTeX code generation
├── templates/            # LaTeX templates
│   └── examples/         # Example optical diagrams
└── main.py               # Main entry point

# Top-level docs
/docs
├── README.md                 # Docs index
└── component-reference.md    # Component reference
```

## Building Diagrams

The tool can generate both LaTeX files and PDFs directly:

1. Design your optical system using the GUI
2. Click "Generate LaTeX" to save the LaTeX code
3. Click "Export PDF" to directly create a PDF

## Notes from Original Documentation

The imaging system is designed to demonstrate optical principles in a laser-based setup. Key components include:

- **Light Source**: A 1064 nm laser that provides the initial beam
- **Beam Expander**: Expands the beam to the desired diameter
- **Focusing Optics**: Controls the beam focus and shape
- **Imaging Lenses**: Creates the desired image magnification and quality
- **Detection System**: Collects the final image or measurement
