"""
LatexGenerator - Handles LaTeX code generation for optical diagrams
"""

import os
from tkinter import filedialog, messagebox

class LatexGenerator:
    """Class for generating LaTeX code from diagram components."""
    
    def generate_latex_code(self, components):
        """Generate LaTeX code from current diagram."""
        latex = "\\documentclass{standalone}\n\\usepackage{pst-optexp}\n\n\\begin{document}\n\n"
        latex += "% Optical Diagram Generated with Optical Diagram Creator\n"
        latex += "\\begin{pspicture}(-2,-2)(12,6)\n"
        latex += "    % Node definitions\n"
        
        # Generate node definitions
        if components:
            latex += "    \\pnodes"
            for i, component in enumerate(components):
                x, y = component['position']
                # Scale canvas coordinates to LaTeX coordinates
                latex_x = x / 50  # Adjust scaling factor as needed
                latex_y = y / 50
                latex += f"({latex_x:.2f},{latex_y:.2f}){{Node{i}}}"
            latex += "\n\n"
        else:
            # Default nodes if no components
            latex += "    \\pnodes(0,0){Start}(5,0){Middle}(10,0){End}\n\n"
        
        latex += "    \\begin{optexp}\n"
        
        # Track beam splitters for special handling of beam paths
        beam_splitters = []
        
        # Add components with proper pst-optexp syntax
        if components:
            for i, component in enumerate(components):
                latex += f"        % {component['name']}\n"
                
                # Customize component rendering based on type
                component_type = component['name']
                
                # Component-specific LaTeX code with proper pst-optexp settings
                if "Lens" in component_type:
                    # Handle lens differently based on position
                    if i == 0:  # First component
                        next_idx = min(i+1, len(components)-1)
                        if "Thick" in component_type:
                            latex += f"        \\lens[lensradius=1, lenstype=thick](Node{i})(Node{next_idx}){{{component['params']['label']}}}\n"
                        elif "Objective" in component_type:
                            latex += f"        \\lens[lensradius=1.2, lenstype=objective](Node{i})(Node{next_idx}){{{component['params']['label']}}}\n"
                        else:
                            latex += f"        \\lens[lensradius=1](Node{i})(Node{next_idx}){{{component['params']['label']}}}\n"
                    elif i == len(components) - 1:  # Last component
                        if "Thick" in component_type:
                            latex += f"        \\lens[lensradius=1, lenstype=thick](Node{i-1})(Node{i}){{{component['params']['label']}}}\n"
                        elif "Objective" in component_type:
                            latex += f"        \\lens[lensradius=1.2, lenstype=objective](Node{i-1})(Node{i}){{{component['params']['label']}}}\n"
                        else:
                            latex += f"        \\lens[lensradius=1](Node{i-1})(Node{i}){{{component['params']['label']}}}\n"
                    else:  # Middle components
                        if "Thick" in component_type:
                            latex += f"        \\lens[lensradius=1, lenstype=thick](Node{i-1})(Node{i+1}){{{component['params']['label']}}}\n"
                        elif "Objective" in component_type:
                            latex += f"        \\lens[lensradius=1.2, lenstype=objective](Node{i-1})(Node{i+1}){{{component['params']['label']}}}\n"
                        else:
                            latex += f"        \\lens[lensradius=1](Node{i-1})(Node{i+1}){{{component['params']['label']}}}\n"
                
                elif "Mirror" in component_type:
                    # Proper mirror representation with angle
                    if i == 0:  # First component
                        next_idx = min(i+1, len(components)-1)
                        if "Curved" in component_type:
                            latex += f"        \\mirror[mirrortype=curved, mirrorradius=30](Node{i})(Node{next_idx}){{{component['params']['label']}}}\n"
                        else:
                            latex += f"        \\mirror[mirrortype=extended](Node{i})(Node{next_idx}){{{component['params']['label']}}}\n"
                    elif i == len(components) - 1:  # Last component
                        if "Curved" in component_type:
                            latex += f"        \\mirror[mirrortype=curved, mirrorradius=30](Node{i-1})(Node{i}){{{component['params']['label']}}}\n"
                        else:
                            latex += f"        \\mirror[mirrortype=extended](Node{i-1})(Node{i}){{{component['params']['label']}}}\n"
                    else:  # Middle components
                        if "Curved" in component_type:
                            latex += f"        \\mirror[mirrortype=curved, mirrorradius=30](Node{i-1})(Node{i+1}){{{component['params']['label']}}}\n"
                        else:
                            latex += f"        \\mirror[mirrortype=extended](Node{i-1})(Node{i+1}){{{component['params']['label']}}}\n"
                
                elif "Beam Splitter" in component_type or "BS" in component_type:
                    # Proper beam splitter with reflection/transmission ratios
                    # Track beam splitters for special beam path handling
                    beam_splitters.append(i)
                    
                    if i == 0:  # First component
                        next_idx = min(i+1, len(components)-1)
                        if "Polarizing" in component_type or "PBS" in component_type:
                            latex += f"        \\beamsplitter[bsstyle=cube](Node{i})(Node{next_idx}){{{component['params']['label']}}}\n"
                        else:
                            latex += f"        \\beamsplitter[bsstyle=plate](Node{i})(Node{next_idx}){{{component['params']['label']}}}\n"
                    elif i == len(components) - 1:  # Last component
                        if "Polarizing" in component_type or "PBS" in component_type:
                            latex += f"        \\beamsplitter[bsstyle=cube](Node{i-1})(Node{i}){{{component['params']['label']}}}\n"
                        else:
                            latex += f"        \\beamsplitter[bsstyle=plate](Node{i-1})(Node{i}){{{component['params']['label']}}}\n"
                    else:  # Middle components
                        if "Polarizing" in component_type or "PBS" in component_type:
                            latex += f"        \\beamsplitter[bsstyle=cube](Node{i-1})(Node{i+1}){{{component['params']['label']}}}\n"
                        else:
                            latex += f"        \\beamsplitter[bsstyle=plate](Node{i-1})(Node{i+1}){{{component['params']['label']}}}\n"
                
                elif "Wave Plate" in component_type or "WP" in component_type:
                    # Wave plate handling
                    if i == 0:  # First component
                        next_idx = min(i+1, len(components)-1)
                        if "Half" in component_type or "HWP" in component_type:
                            latex += f"        \\optretplate[platetype=half](Node{i})(Node{next_idx}){{{component['params']['label']}}}\n"
                        else:
                            latex += f"        \\optretplate[platetype=quarter](Node{i})(Node{next_idx}){{{component['params']['label']}}}\n"
                    elif i == len(components) - 1:  # Last component
                        if "Half" in component_type or "HWP" in component_type:
                            latex += f"        \\optretplate[platetype=half](Node{i-1})(Node{i}){{{component['params']['label']}}}\n"
                        else:
                            latex += f"        \\optretplate[platetype=quarter](Node{i-1})(Node{i}){{{component['params']['label']}}}\n"
                    else:  # Middle components
                        if "Half" in component_type or "HWP" in component_type:
                            latex += f"        \\optretplate[platetype=half](Node{i-1})(Node{i+1}){{{component['params']['label']}}}\n"
                        else:
                            latex += f"        \\optretplate[platetype=quarter](Node{i-1})(Node{i+1}){{{component['params']['label']}}}\n"
                
                elif "Isolator" in component_type:
                    # Optical isolator
                    if i == 0:  # First component
                        next_idx = min(i+1, len(components)-1)
                        latex += f"        \\optisolator(Node{i})(Node{next_idx}){{{component['params']['label']}}}\n"
                    elif i == len(components) - 1:  # Last component
                        latex += f"        \\optisolator(Node{i-1})(Node{i}){{{component['params']['label']}}}\n"
                    else:  # Middle components
                        latex += f"        \\optisolator(Node{i-1})(Node{i+1}){{{component['params']['label']}}}\n"
                
                elif "Modulator" in component_type or "AOM" in component_type:
                    # AOM handling
                    if i == 0:  # First component
                        next_idx = min(i+1, len(components)-1)
                        latex += f"        \\aom(Node{i})(Node{next_idx}){{{component['params']['label']}}}\n"
                    elif i == len(components) - 1:  # Last component
                        latex += f"        \\aom(Node{i-1})(Node{i}){{{component['params']['label']}}}\n"
                    else:  # Middle components
                        latex += f"        \\aom(Node{i-1})(Node{i+1}){{{component['params']['label']}}}\n"
                
                elif "EOM" in component_type:
                    # EOM handling
                    if i == 0:  # First component
                        next_idx = min(i+1, len(components)-1)
                        latex += f"        \\eom(Node{i})(Node{next_idx}){{{component['params']['label']}}}\n"
                    elif i == len(components) - 1:  # Last component
                        latex += f"        \\eom(Node{i-1})(Node{i}){{{component['params']['label']}}}\n"
                    else:  # Middle components
                        latex += f"        \\eom(Node{i-1})(Node{i+1}){{{component['params']['label']}}}\n"
                
                elif "Filter" in component_type:
                    # Filter handling
                    filter_type = "nd"  # default
                    if "Bandpass" in component_type:
                        filter_type = "bandpass"
                    
                    if i == 0:  # First component
                        next_idx = min(i+1, len(components)-1)
                        latex += f"        \\optfilter[filtertype={filter_type}](Node{i})(Node{next_idx}){{{component['params']['label']}}}\n"
                    elif i == len(components) - 1:  # Last component
                        latex += f"        \\optfilter[filtertype={filter_type}](Node{i-1})(Node{i}){{{component['params']['label']}}}\n"
                    else:  # Middle components
                        latex += f"        \\optfilter[filtertype={filter_type}](Node{i-1})(Node{i+1}){{{component['params']['label']}}}\n"
                
                elif "Grating" in component_type:
                    # Grating handling
                    if i == 0:  # First component
                        next_idx = min(i+1, len(components)-1)
                        latex += f"        \\optgrating[gratingwidth={component['params'].get('gratingwidth', '1.5')}](Node{i})(Node{next_idx}){{{component['params']['label']}}}\n"
                    elif i == len(components) - 1:  # Last component
                        latex += f"        \\optgrating[gratingwidth={component['params'].get('gratingwidth', '1.5')}](Node{i-1})(Node{i}){{{component['params']['label']}}}\n"
                    else:  # Middle components
                        latex += f"        \\optgrating[gratingwidth={component['params'].get('gratingwidth', '1.5')}](Node{i-1})(Node{i+1}){{{component['params']['label']}}}\n"
                
                elif "Fiber" in component_type:
                    # Fiber handling
                    if i == 0:  # First component
                        next_idx = min(i+1, len(components)-1)
                        latex += f"        \\optfiber[fibertype=patch](Node{i})(Node{next_idx}){{{component['params']['label']}}}\n"
                    elif i == len(components) - 1:  # Last component
                        latex += f"        \\optfiber[fibertype=patch](Node{i-1})(Node{i}){{{component['params']['label']}}}\n"
                    else:  # Middle components
                        latex += f"        \\optfiber[fibertype=patch](Node{i-1})(Node{i+1}){{{component['params']['label']}}}\n"
                
                elif "Circulator" in component_type:
                    # Optical circulator
                    if i == 0:  # First component
                        next_idx = min(i+1, len(components)-1)
                        latex += f"        \\optcirculator(Node{i})(Node{next_idx}){{{component['params']['label']}}}\n"
                    elif i == len(components) - 1:  # Last component
                        latex += f"        \\optcirculator(Node{i-1})(Node{i}){{{component['params']['label']}}}\n"
                    else:  # Middle components
                        latex += f"        \\optcirculator(Node{i-1})(Node{i+1}){{{component['params']['label']}}}\n"
                
                elif "Amplifier" in component_type:
                    # Optical amplifier
                    if i == 0:  # First component
                        next_idx = min(i+1, len(components)-1)
                        latex += f"        \\optamplifier(Node{i})(Node{next_idx}){{{component['params']['label']}}}\n"
                    elif i == len(components) - 1:  # Last component
                        latex += f"        \\optamplifier(Node{i-1})(Node{i}){{{component['params']['label']}}}\n"
                    else:  # Middle components
                        latex += f"        \\optamplifier(Node{i-1})(Node{i+1}){{{component['params']['label']}}}\n"
                
                elif "Source" in component_type or "Laser" in component_type:
                    # Light source components
                    next_idx = min(i+1, len(components)-1)
                    latex += f"        \\optbox[position=start, innerlabel, optboxwidth=1.2](Node{i})(Node{next_idx}){{{component['params']['label']}}}\n"
                
                elif "Detector" in component_type or "Photodiode" in component_type or "Camera" in component_type or "Spectrometer" in component_type:
                    # Detector components
                    if "Block" in component_type:
                        # Special case for beam block
                        latex += f"        \\optdetector[dettype=block](Node{i-1})(Node{i}){{{component['params']['label']}}}\n"
                    else:
                        latex += f"        \\optbox[position=end, innerlabel, optboxwidth=1.2](Node{i-1})(Node{i}){{{component['params']['label']}}}\n"
                
                else:
                    # Generic component handling with standard pst-optexp syntax
                    if i == 0:  # First component
                        next_idx = min(i+1, len(components)-1)
                        latex += f"        {component['latex']}(Node{i})(Node{next_idx}){{{component['params']['label']}}}\n"
                    elif i == len(components) - 1:  # Last component
                        latex += f"        {component['latex']}(Node{i-1})(Node{i}){{{component['params']['label']}}}\n"
                    else:  # Middle components
                        latex += f"        {component['latex']}(Node{i-1})(Node{i+1}){{{component['params']['label']}}}\n"
        else:
            # Placeholder comment if no components
            latex += "        % Add components to your diagram\n"
        
        # Beam path with proper pst-optexp settings
        latex += "\n        % Beam paths\n"
        
        if len(components) >= 2:
            # Set beam style properties using pst-optexp
            latex += "        \\addtopsstyle{Beam}{linestyle=none, fillstyle=solid, fillcolor=red}\n"
            
            # Handle beam paths based on component types
            if beam_splitters:
                # If we have beam splitters, create a more complex beam path system
                # First, draw beam from source to first beam splitter
                first_bs_idx = beam_splitters[0]
                if first_bs_idx > 0:
                    latex += f"        \\drawwidebeam[beamwidth=0.1](Node0)(Node{first_bs_idx})\n"
                
                # For each beam splitter, create transmitted and reflected beams
                for bs_idx in beam_splitters:
                    # Only process if not the last component
                    if bs_idx < len(components) - 1:
                        # Create a transmitted beam (straight through)
                        if bs_idx + 1 < len(components):
                            next_component = bs_idx + 1
                            latex += f"        \\drawwidebeam[beamwidth=0.1](Node{bs_idx})(Node{next_component})\n"
                        
                        # Create a reflected beam if there's space for it (optional in future enhancements)
                        # This would require additional node definitions and component layout logic
                
                # Connect any remaining components after the last beam splitter
                last_bs_idx = beam_splitters[-1]
                if last_bs_idx < len(components) - 2:
                    latex += f"        \\drawwidebeam[beamwidth=0.1](Node{last_bs_idx+1})(Node{len(components)-1})\n"
            else:
                # For setups without beam splitters, draw direct paths between components
                if len(components) == 2:
                    # Simple direct beam between two components
                    latex += "        \\drawwidebeam[beamwidth=0.1](Node0)(Node1)\n"
                else:
                    # For more complex setups, draw segments between each component
                    for i in range(len(components) - 1):
                        # Customize beam style based on component types
                        if "Lens" in components[i]['name'] or "Lens" in components[i+1]['name']:
                            # Use a focusing/diverging beam for lenses
                            latex += f"        \\drawresizeabeam[beamwidth=0.15, beamendwidth=0.07](Node{i})(Node{i+1})\n"
                        elif "Filter" in components[i]['name'] or "Filter" in components[i+1]['name']:
                            # Use a colored beam for filters
                            if "Bandpass" in components[i]['name'] or "Bandpass" in components[i+1]['name']:
                                latex += f"        \\drawwidebeam[beamwidth=0.1, beamcolor=green!70](Node{i})(Node{i+1})\n"
                            else:
                                latex += f"        \\drawwidebeam[beamwidth=0.08, beamcolor=red!70](Node{i})(Node{i+1})\n"
                        elif "Fiber" in components[i]['name'] or "Fiber" in components[i+1]['name']:
                            # Use a narrow beam for fiber connections
                            latex += f"        \\drawnarrowbeam[beamwidth=0.05](Node{i})(Node{i+1})\n"
                        else:
                            # Default wide beam
                            latex += f"        \\drawwidebeam[beamwidth=0.1](Node{i})(Node{i+1})\n"
        else:
            # Default path for when there are less than 2 components
            latex += "        % Need at least 2 components to draw a beam\n"
            
        latex += "    \\end{optexp}\n"
        latex += "\\end{pspicture}\n\n"
        latex += "\\end{document}"
        
        return latex
    
    def save_latex_file(self, components):
        """Save the LaTeX code to a file."""
        latex_code = self.generate_latex_code(components)
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".tex",
            filetypes=[("LaTeX files", "*.tex"), ("All files", "*.*")],
            initialdir=os.path.join(os.getcwd(), "src", "templates")
        )
        
        if file_path:
            with open(file_path, 'w') as f:
                f.write(latex_code)
            messagebox.showinfo("Success", f"LaTeX file saved to {file_path}") 