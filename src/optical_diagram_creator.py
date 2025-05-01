#!/usr/bin/env python3
"""
Optical Diagram Creator - GUI Tool for LaTeX Optical Diagrams

This tool provides a graphical interface for creating optical diagrams
using the pst-optexp LaTeX package. It allows drag-and-drop placement
of optical components, configuration of their properties, and automatic
generation of LaTeX code with PDF output.
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

class OpticalDiagramCreator:
    """Main application class for the Optical Diagram Creator."""
    
    def __init__(self, root):
        """Initialize the application."""
        self.root = root
        self.root.title("Optical Diagram Creator")
        self.root.geometry("1200x800")
        
        # Set up the main frame structure
        self.setup_ui()
        
        # Component library - defined as tuples (display_name, LaTeX command, params)
        self.components = {
            "Light Sources": [
                ("Laser Source", "\\optbox[position=start, innerlabel, optboxwidth=1.2]", 
                {"wavelength": "1064", "label": "Laser"}),
                ("LED Source", "\\optbox[position=start, innerlabel, optboxwidth=1.2]", 
                {"wavelength": "650", "label": "LED"})
            ],
            "Optical Components": [
                ("Lens", "\\lens", {"label": "Lens", "focal_length": "50"}),
                ("Mirror", "\\mirror", {"label": "Mirror", "angle": "45"}),
                ("Beam Splitter", "\\beamsplitter", {"label": "BS", "ratio": "50:50"}),
                ("Half-Wave Plate", "\\optretplate", {"label": "HWP"})
            ],
            "Detectors": [
                ("Photodiode", "\\optbox[position=end, innerlabel, optboxwidth=1.2]", 
                {"label": "PD"}),
                ("Camera", "\\optbox[position=end, innerlabel, optboxwidth=1.2]", 
                {"label": "Camera"})
            ]
        }
        
        # Load components into the library panel
        self.load_component_library()
        
        # Current diagram data
        self.diagram_components = []
        self.selected_component = None
        
        # Canvas setup
        self.canvas_setup()
        
    def setup_ui(self):
        """Set up the main UI layout."""
        # Create main frame containers
        self.left_panel = ttk.Frame(self.root, padding="10")
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5, pady=5)
        
        self.center_panel = ttk.Frame(self.root, padding="10")
        self.center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.right_panel = ttk.Frame(self.root, padding="10")
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=5, pady=5)
        
        # Left panel - Component library
        ttk.Label(self.left_panel, text="Component Library", font=('Arial', 12, 'bold')).pack(anchor=tk.W)
        self.component_tree = ttk.Treeview(self.left_panel)
        self.component_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Button to add selected component
        ttk.Button(self.left_panel, text="Add Component", 
                  command=self.add_selected_component).pack(fill=tk.X, pady=5)
        
        # Center panel - Diagram canvas
        ttk.Label(self.center_panel, text="Diagram Canvas", font=('Arial', 12, 'bold')).pack(anchor=tk.W)
        self.canvas_frame = ttk.Frame(self.center_panel, relief=tk.SUNKEN, borderwidth=1)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Canvas toolbar
        self.toolbar = ttk.Frame(self.center_panel)
        self.toolbar.pack(fill=tk.X, pady=5)
        
        ttk.Button(self.toolbar, text="Generate LaTeX", 
                  command=self.generate_latex).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.toolbar, text="Export PDF", 
                  command=self.export_pdf).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.toolbar, text="Clear Canvas", 
                  command=self.clear_canvas).pack(side=tk.LEFT, padx=5)
        
        # Right panel - Properties and LaTeX preview
        ttk.Label(self.right_panel, text="Properties", font=('Arial', 12, 'bold')).pack(anchor=tk.W)
        self.properties_frame = ttk.Frame(self.right_panel)
        self.properties_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(self.right_panel, text="LaTeX Code", font=('Arial', 12, 'bold')).pack(anchor=tk.W)
        self.latex_preview = scrolledtext.ScrolledText(self.right_panel, height=15)
        self.latex_preview.pack(fill=tk.BOTH, expand=True, pady=5)
        
    def load_component_library(self):
        """Load available components into the tree view."""
        self.component_tree.delete(*self.component_tree.get_children())
        
        for category, components in self.components.items():
            category_id = self.component_tree.insert("", "end", text=category)
            for component in components:
                name = component[0]
                self.component_tree.insert(category_id, "end", text=name, values=(name,))
        
    def add_selected_component(self):
        """Add the selected component from the library to the diagram."""
        selection = self.component_tree.selection()
        if not selection:
            messagebox.showinfo("Selection Required", "Please select a component from the library first.")
            return
            
        item = self.component_tree.item(selection[0])
        parent = self.component_tree.parent(selection[0])
        
        # Only add if it's a component, not a category
        if parent:
            component_name = item['text']
            
            # Find the component in our library
            category = self.component_tree.item(parent)['text']
            for comp in self.components[category]:
                if comp[0] == component_name:
                    # Add to our diagram components list
                    # Real implementation would add to canvas
                    self.diagram_components.append({
                        'name': comp[0],
                        'latex': comp[1],
                        'params': comp[2].copy(),
                        'position': (100, 100)  # Default position
                    })
                    
                    messagebox.showinfo("Component Added", f"Added {component_name} to diagram")
                    self.update_latex_preview()
                    break
    
    def canvas_setup(self):
        """Set up the canvas for the diagram."""
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Placeholder for now - would implement actual drawing and interaction here
        self.canvas.create_text(150, 150, text="Canvas will display optical diagram here")
        
    def update_latex_preview(self):
        """Update the LaTeX code preview based on current components."""
        latex_code = self.generate_latex_code()
        self.latex_preview.delete(1.0, tk.END)
        self.latex_preview.insert(tk.END, latex_code)
        
    def generate_latex_code(self):
        """Generate LaTeX code from current diagram."""
        latex = "\\documentclass{standalone}\n\\usepackage{pst-optexp}\n\n\\begin{document}\n\n"
        latex += "% Optical Diagram Generated with Optical Diagram Creator\n"
        latex += "\\begin{pspicture}(-2,-2)(12,6)\n"
        latex += "    % Node definitions\n"
        
        # Placeholder for node definitions
        latex += "    \\pnodes(0,0){Start}(5,0){Middle}(10,0){End}\n\n"
        
        latex += "    \\begin{optexp}\n"
        
        # Add components
        for i, component in enumerate(self.diagram_components):
            latex += f"        % {component['name']}\n"
            if i == 0:
                latex += f"        {component['latex']}(Start)(Middle){{{component['params']['label']}}}\n"
            elif i == len(self.diagram_components) - 1:
                latex += f"        {component['latex']}(Middle)(End){{{component['params']['label']}}}\n"
            else:
                # This is simplified; real implementation would calculate proper connections
                latex += f"        % Connection would be properly defined here\n"
        
        # If no components, add placeholder comment
        if not self.diagram_components:
            latex += "        % Add components to your diagram\n"
        
        latex += "        % Beam paths\n"
        latex += "        \\addtopsstyle{Beam}{linestyle=none, fillstyle=solid, fillcolor=red}\n"
        latex += "        \\drawwidebeam[beamwidth=0.1]{1-3}\n"
        latex += "    \\end{optexp}\n"
        latex += "\\end{pspicture}\n\n"
        latex += "\\end{document}"
        
        return latex
        
    def generate_latex(self):
        """Generate LaTeX file from current diagram."""
        latex_code = self.generate_latex_code()
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".tex",
            filetypes=[("LaTeX files", "*.tex"), ("All files", "*.*")],
            initialdir=os.path.join(os.getcwd(), "src", "schematics")
        )
        
        if file_path:
            with open(file_path, 'w') as f:
                f.write(latex_code)
            messagebox.showinfo("Success", f"LaTeX file saved to {file_path}")
            
    def export_pdf(self):
        """Export the current diagram as a PDF."""
        # Temporary file approach
        with tempfile.NamedTemporaryFile(suffix='.tex', delete=False) as tmp:
            tmp_path = tmp.name
            tmp.write(self.generate_latex_code().encode('utf-8'))
        
        try:
            # Run xelatex on the temporary file
            result = subprocess.run(
                ['xelatex', '-output-directory', os.path.dirname(tmp_path), tmp_path],
                capture_output=True, text=True, check=True
            )
            
            # Get the PDF path
            pdf_path = tmp_path.replace('.tex', '.pdf')
            
            if os.path.exists(pdf_path):
                # Ask where to save the PDF
                save_path = filedialog.asksaveasfilename(
                    defaultextension=".pdf",
                    filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                    initialdir=os.path.join(os.getcwd(), "build", "schematics")
                )
                
                if save_path:
                    # Copy the PDF to the chosen location
                    with open(pdf_path, 'rb') as src, open(save_path, 'wb') as dst:
                        dst.write(src.read())
                    messagebox.showinfo("Success", f"PDF exported to {save_path}")
            else:
                messagebox.showerror("Error", "PDF generation failed")
                
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"LaTeX compilation failed: {e.stderr}")
        finally:
            # Clean up temporary files
            for ext in ['.tex', '.pdf', '.aux', '.log']:
                try:
                    os.unlink(tmp_path.replace('.tex', ext))
                except:
                    pass
    
    def clear_canvas(self):
        """Clear all components from the canvas."""
        self.diagram_components = []
        self.update_latex_preview()
        messagebox.showinfo("Canvas Cleared", "All components have been removed from the diagram")

def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = OpticalDiagramCreator(root)
    root.mainloop()

if __name__ == "__main__":
    main() 