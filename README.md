# Laser Optics Schematic Projects

This repository contains LaTeX projects for creating optical schematic diagrams using PSTricks and the pst-optexp package.

## Project Structure

```
.
├── projects/                # Main projects directory
│   ├── basic_laser/         # Basic laser setup project
│   │   ├── schematics/      # Schematic diagrams
│   │   ├── tests/           # Test files
│   │   └── docs/            # Documentation
│   └── advanced_imaging/    # Advanced imaging system project
│       ├── schematics/      # Schematic diagrams
│       ├── tests/           # Test files
│       └── docs/            # Documentation
├── common/                  # Common resources
│   ├── cheatsheets/         # Reference cheatsheets
│   └── templates/           # Template files
└── build/                   # Output directory (created by make)
    ├── basic_laser/         # Built PDFs for basic_laser
    ├── advanced_imaging/    # Built PDFs for advanced_imaging
    └── common/              # Built PDFs for common resources
```

## Prerequisites

- LaTeX distribution (TeXLive or MikTeX recommended)
- PSTricks packages
- pst-optexp package for optical schematics

## Usage

### Building Projects

```bash
# Build default example
make

# Build all projects
make all-projects

# Build a specific project
make project-basic_laser
make project-advanced_imaging

# Build common resources
make cheatsheets

# Clean build artifacts
make clean
```

### Adding New Projects

1. Create a new project directory under `projects/`:

```bash
mkdir -p projects/my_new_project/{schematics,tests,docs}
```

2. Add the project name to the `PROJECTS` variable in the Makefile:

```makefile
PROJECTS := basic_laser advanced_imaging my_new_project
```

3. Add your LaTeX files to the appropriate directories under your project.

## Example Projects

### Basic Laser

A simple laser setup with a laser source, lens, and screen.

### Advanced Imaging

A more complex optical system for imaging applications.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 