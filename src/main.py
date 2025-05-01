#!/usr/bin/env python3
"""
Optical Diagram Creator - GUI Tool for LaTeX Optical Diagrams

This tool provides a graphical interface for creating optical diagrams
using the pst-optexp LaTeX package. It allows drag-and-drop placement
of optical components, configuration of their properties, and automatic
generation of LaTeX code with PDF output.
"""

import tkinter as tk
from app.gui.application import OpticalDiagramCreator

def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = OpticalDiagramCreator(root)
    root.mainloop()

if __name__ == "__main__":
    main() 