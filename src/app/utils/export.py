"""
Export - Handles PDF exporting and other export functions
"""

import os
import tempfile
import subprocess
from tkinter import filedialog, messagebox

class PDFExporter:
    """Class for exporting diagrams as PDFs using LaTeX."""
    
    def export_pdf(self, latex_code):
        """Export the current diagram as a PDF."""
        # Create a temporary directory for the LaTeX build
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create a temporary file for the LaTeX code
            tmp_path = os.path.join(tmp_dir, "diagram.tex")
            with open(tmp_path, 'w') as tmp:
                tmp.write(latex_code)
            
            try:
                # Run xelatex on the temporary file
                process = subprocess.run(
                    ['xelatex', '-output-directory', tmp_dir, tmp_path],
                    capture_output=True, text=True, check=True
                )
                
                # Get the PDF path
                pdf_path = os.path.join(tmp_dir, "diagram.pdf")
                
                if os.path.exists(pdf_path):
                    # Ask where to save the PDF
                    save_path = filedialog.asksaveasfilename(
                        defaultextension=".pdf",
                        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                        initialdir=os.path.join(os.getcwd(), "output")
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
                
    def export_png(self, latex_code):
        """Export the current diagram as a PNG image (future feature)."""
        # This is a placeholder for future PNG export functionality
        messagebox.showinfo("Feature Not Available", "PNG export will be implemented in a future version") 