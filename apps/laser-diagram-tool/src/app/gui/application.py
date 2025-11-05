"""
OpticalDiagramCreator - Main application class for the Optical Diagram Creator.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import re
from app.gui.canvas_manager import CanvasManager
from app.gui.component_library import ComponentLibrary
from app.utils.latex_generator import LatexGenerator
from app.utils.export import PDFExporter
from app.utils.latex_parser import LatexParser

class OpticalDiagramCreator:
    """Main application class for the Optical Diagram Creator."""
    
    def __init__(self, root):
        """Initialize the application."""
        self.root = root
        self.root.title("Optical Diagram Creator")
        self.root.geometry("1200x800")
        
        # Component library
        self.component_library = ComponentLibrary()
        
        # Current diagram data
        self.diagram_components = []
        self.selected_component = None
        
        # Set up the main frame structure
        self.setup_ui()
        
        # Initialize the canvas manager
        self.canvas_manager = CanvasManager(self.canvas, self.diagram_components)
        
        # Initialize LaTeX generator
        self.latex_generator = LatexGenerator()
        
        # Initialize LaTeX parser
        self.latex_parser = LatexParser()
        
        # Initialize PDF exporter
        self.pdf_exporter = PDFExporter()
        
        # Flag to prevent update loops when editing LaTeX
        self.updating_latex = False
        
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
        
        # Right panel - Properties and LaTeX preview/editor
        ttk.Label(self.right_panel, text="Properties", font=('Arial', 12, 'bold')).pack(anchor=tk.W)
        self.properties_frame = ttk.Frame(self.right_panel)
        self.properties_frame.pack(fill=tk.X, pady=5)
        
        # LaTeX editor section
        latex_frame = ttk.Frame(self.right_panel)
        latex_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        latex_header = ttk.Frame(latex_frame)
        latex_header.pack(fill=tk.X)
        
        ttk.Label(latex_header, text="LaTeX Code", font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        ttk.Button(latex_header, text="Apply Changes", command=self.apply_latex_changes).pack(side=tk.RIGHT)
        
        # LaTeX editor with syntax highlighting (future enhancement)
        self.latex_preview = scrolledtext.ScrolledText(latex_frame, height=20, font=('Courier', 10))
        self.latex_preview.pack(fill=tk.BOTH, expand=True)
        
        # Add key bindings for common editor features
        self.latex_preview.bind("<Tab>", self.handle_tab)
        
        # Canvas setup
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Load components into the library panel
        self.component_library.load_components_to_tree(self.component_tree)
        
    def handle_tab(self, event):
        """Handle tab key in the LaTeX editor to insert spaces or indent selected lines."""
        try:
            # Check if there is a selection
            start, end = self.latex_preview.tag_ranges(tk.SEL)

            # Get the selected text
            selected_text = self.latex_preview.get(start, end)

            # Indent each line of the selection
            indented_text = ""
            for line in selected_text.split('\n'):
                indented_text += "    " + line + "\n"

            # Remove the final newline if the original selection didn't have one
            if not selected_text.endswith('\n'):
                indented_text = indented_text.rstrip('\n')

            # Replace the selection with the indented text
            self.latex_preview.delete(start, end)
            self.latex_preview.insert(start, indented_text)

        except tk.TclError:
            # No selection, so just insert 4 spaces
            self.latex_preview.insert(tk.INSERT, "    ")

        return "break"  # Prevent default tab behavior
        
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
            component = self.component_library.get_component_by_name(component_name)
            
            if component:
                # Check if this is a complex optical setup
                if self.component_library.is_complex_setup(component_name):
                    self.add_complex_setup(component_name)
                else:
                    # Add standard component to our diagram components list
                    self.diagram_components.append({
                        'name': component[0],
                        'latex': component[1],
                        'params': component[2].copy(),
                        'position': (100, 100)  # Default position
                    })
                    
                    # Update the canvas and preview
                    self.canvas_manager.redraw_canvas()
                    self.update_latex_preview()
                    messagebox.showinfo("Component Added", f"Added {component_name} to diagram")
    
    def add_complex_setup(self, setup_name):
        """Add a predefined complex optical setup to the diagram."""
        # Get the components and beam definitions for this setup
        setup_components, setup_beams = self.component_library.get_setup_components(setup_name)
        
        if not setup_components:
            messagebox.showerror("Error", f"Failed to get components for {setup_name}")
            return
        
        # Store current component count to calculate new indices
        start_idx = len(self.diagram_components)
        
        # Create a temporary storage for new components
        new_components = []
        
        # Add each component from the setup
        for comp in setup_components:
            component_type = comp["type"]
            position = comp["position"]
            params = comp["params"]
            
            # Get the component template
            template = self.component_library.get_component_by_name(component_type)
            
            if template:
                # Create component based on template but with our specified params
                new_components.append({
                    'name': component_type,
                    'latex': template[1],
                    'params': params,
                    'position': position
                })
            else:
                messagebox.showwarning("Warning", f"Component type {component_type} not found")
        
        # Add all new components to the diagram
        self.diagram_components.extend(new_components)
        
        # Update the canvas and preview
        self.canvas_manager.redraw_canvas()
        self.update_latex_preview()
        
        messagebox.showinfo("Setup Added", f"Added {setup_name} with {len(new_components)} components")
    
    def update_latex_preview(self):
        """Update the LaTeX code preview based on current components."""
        if self.updating_latex:
            return
            
        self.updating_latex = True
        latex_code = self.latex_generator.generate_latex_code(self.diagram_components)
        self.latex_preview.delete(1.0, tk.END)
        self.latex_preview.insert(tk.END, latex_code)
        self.updating_latex = False
        
    def apply_latex_changes(self):
        """Apply the LaTeX code changes to update the diagram."""
        try:
            # Get the current LaTeX code from the editor
            latex_code = self.latex_preview.get(1.0, tk.END)
            
            # Parse the LaTeX code to extract components and their properties
            components = self.latex_parser.parse_latex_code(latex_code)
            
            if components:
                # Update the diagram components
                self.diagram_components = components
                
                # Redraw the canvas
                self.canvas_manager.redraw_canvas()
                
                messagebox.showinfo("Success", "LaTeX code changes applied successfully")
            else:
                messagebox.showwarning("Warning", "Could not parse any components from the LaTeX code")
        except Exception as e:
            messagebox.showerror("Error", f"Error parsing LaTeX code: {str(e)}")
    
    def generate_latex(self):
        """Generate LaTeX file from current diagram."""
        self.latex_generator.save_latex_file(self.diagram_components)
            
    def export_pdf(self):
        """Export the current diagram as a PDF."""
        # Get the current LaTeX code from the editor instead of generating
        # This allows users to export their manually edited LaTeX
        latex_code = self.latex_preview.get(1.0, tk.END)
        self.pdf_exporter.export_pdf(latex_code)
                
    def clear_canvas(self):
        """Clear the canvas and reset components."""
        self.diagram_components.clear()
        self.canvas_manager.redraw_canvas()
        self.update_latex_preview() 