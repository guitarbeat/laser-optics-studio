"""
CanvasManager - Handles the drawing and interaction with the diagram canvas
"""

import tkinter as tk

class CanvasManager:
    """Class to manage the diagram canvas and component rendering."""
    
    def __init__(self, canvas, components_list):
        """Initialize with the canvas and components list."""
        self.canvas = canvas
        self.components = components_list
        self.canvas_objects = []
        
        # Set up canvas interactions
        self.setup_canvas_interactions()
        
    def setup_canvas_interactions(self):
        """Set up mouse and keyboard interactions for the canvas."""
        # Drag and drop functionality for components
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        
        # Selection functionality
        self.selected_item = None
        self.drag_start_x = 0
        self.drag_start_y = 0
        
    def redraw_canvas(self):
        """Redraw all components on the canvas."""
        # Clear the canvas
        self.canvas.delete("all")
        self.canvas_objects = []
        
        # If no components, draw placeholder text
        if not self.components:
            self.canvas.create_text(
                self.canvas.winfo_width() // 2,
                self.canvas.winfo_height() // 2,
                text="Add components from the library panel",
                fill="gray"
            )
            return
        
        # Draw each component
        for i, component in enumerate(self.components):
            self.draw_component(component, i)
        
        # Draw connections between components
        self.draw_connections()
    
    def draw_component(self, component, index):
        """Draw a single component on the canvas."""
        x, y = component['position']
        component_name = component['name']
        
        # Different drawing methods based on component type
        if "Lens" in component_name:
            if "Thick" in component_name:
                # Draw thick lens
                obj_id = self.canvas.create_oval(x-30, y-40, x+30, y+40, outline="black", width=2)
                self.canvas.create_oval(x-25, y-35, x+25, y+35, outline="black", width=1, dash=(2,2))
                text_id = self.canvas.create_text(x, y, text=component['params']['label'])
            elif "Objective" in component_name:
                # Draw objective lens
                obj_id = self.canvas.create_oval(x-30, y-40, x+30, y+40, outline="black", width=2, fill="light gray")
                text_id = self.canvas.create_text(x, y, text=component['params']['label'])
            else:
                # Draw standard lens as ellipse
                obj_id = self.canvas.create_oval(x-30, y-40, x+30, y+40, outline="black", width=2)
                text_id = self.canvas.create_text(x, y, text=component['params']['label'])
        
        elif "Mirror" in component_name:
            if "Curved" in component_name:
                # Draw curved mirror
                obj_id = self.canvas.create_arc(x-40, y-40, x+40, y+40, 
                                               start=135, extent=90, 
                                               style="arc", outline="black", width=3)
                text_id = self.canvas.create_text(x+10, y-10, text=component['params']['label'])
            else:
                # Draw standard mirror as line
                obj_id = self.canvas.create_line(x-40, y-40, x+40, y+40, fill="black", width=3)
                text_id = self.canvas.create_text(x+10, y-10, text=component['params']['label'])
        
        elif "Beam Splitter" in component_name or "BS" in component_name:
            if "Polarizing" in component_name or "PBS" in component_name:
                # Draw PBS as a cube
                obj_id = self.canvas.create_rectangle(x-30, y-30, x+30, y+30, outline="black", width=2, fill="light gray")
                self.canvas.create_line(x-30, y-30, x+30, y+30, fill="black", width=1)
                text_id = self.canvas.create_text(x, y-40, text=component['params']['label'])
            else:
                # Draw regular beam splitter as a plate
                obj_id = self.canvas.create_rectangle(x-5, y-30, x+5, y+30, outline="black", width=2, fill="light blue")
                self.canvas.create_line(x-30, y, x+30, y, fill="black", width=1, dash=(4,2))
                text_id = self.canvas.create_text(x, y-40, text=component['params']['label'])
        
        elif "Wave Plate" in component_name or "WP" in component_name:
            # Draw wave plate as a rectangle with lines
            obj_id = self.canvas.create_rectangle(x-20, y-30, x+20, y+30, outline="black", width=2, fill="light yellow")
            # Different patterns for half vs quarter wave plates
            if "Half" in component_name or "HWP" in component_name:
                self.canvas.create_line(x-20, y-15, x+20, y-15, fill="black")
                self.canvas.create_line(x-20, y+15, x+20, y+15, fill="black")
            else:
                self.canvas.create_line(x-20, y-10, x+20, y-10, fill="black")
                self.canvas.create_line(x-20, y, x+20, y, fill="black")
                self.canvas.create_line(x-20, y+10, x+20, y+10, fill="black")
            text_id = self.canvas.create_text(x, y, text=component['params']['label'])
        
        elif "Filter" in component_name:
            # Draw filter as a thin rectangle
            obj_id = self.canvas.create_rectangle(x-30, y-7, x+30, y+7, outline="black", width=2, fill="light green")
            text_id = self.canvas.create_text(x, y-20, text=component['params']['label'])
        
        elif "Isolator" in component_name:
            # Draw optical isolator
            obj_id = self.canvas.create_oval(x-25, y-25, x+25, y+25, outline="black", width=2)
            # Draw directional arrow inside
            self.canvas.create_line(x-15, y, x+15, y, fill="black", arrow=tk.LAST, width=2)
            text_id = self.canvas.create_text(x, y-35, text=component['params']['label'])
        
        elif "Modulator" in component_name or "AOM" in component_name or "EOM" in component_name:
            # Draw modulator as rectangle with zigzag line
            obj_id = self.canvas.create_rectangle(x-35, y-25, x+35, y+25, outline="black", width=2)
            # Draw a zigzag line to represent modulation
            points = [x-25, y-10, x-15, y+10, x-5, y-10, x+5, y+10, x+15, y-10, x+25, y+10]
            self.canvas.create_line(points, fill="black", width=1)
            text_id = self.canvas.create_text(x, y-35, text=component['params']['label'])
        
        elif "Grating" in component_name:
            # Draw diffraction grating
            obj_id = self.canvas.create_rectangle(x-30, y-4, x+30, y+4, outline="black", width=1, fill="gray")
            # Add grating lines
            for i in range(-25, 26, 5):
                self.canvas.create_line(x+i, y-7, x+i, y+7, fill="black", width=1)
            text_id = self.canvas.create_text(x, y-15, text=component['params']['label'])
        
        elif "Fiber" in component_name:
            # Draw fiber as curved line
            obj_id = self.canvas.create_arc(x-40, y-40, x+40, y+40, 
                                           start=0, extent=180, 
                                           style="arc", outline="blue", width=2)
            text_id = self.canvas.create_text(x, y+25, text=component['params']['label'])
        
        elif "Source" in component_name or "Laser" in component_name or "LED" in component_name:
            # Draw light source as rectangle with distinctive colors
            if "Laser" in component_name:
                fill_color = "light yellow"
            elif "LED" in component_name:
                fill_color = "light green"
            else:
                fill_color = "white"
            obj_id = self.canvas.create_rectangle(x-40, y-30, x+40, y+30, outline="black", fill=fill_color)
            text_id = self.canvas.create_text(x, y, text=component['params']['label'])
        
        elif "Detector" in component_name or "Photodiode" in component_name or "Camera" in component_name:
            # Draw detector as rectangle with distinctive colors
            if "Camera" in component_name:
                fill_color = "light blue"
                # Add camera lens symbol
                self.canvas.create_oval(x-15, y-15, x+15, y+15, outline="black")
            elif "Spectrometer" in component_name:
                fill_color = "light purple"
            elif "Power" in component_name:
                fill_color = "light green"
            else:
                fill_color = "light gray"
            obj_id = self.canvas.create_rectangle(x-40, y-30, x+40, y+30, outline="black", fill=fill_color)
            text_id = self.canvas.create_text(x, y, text=component['params']['label'])
        
        elif "Circulator" in component_name:
            # Draw optical circulator as circle with curved arrow
            obj_id = self.canvas.create_oval(x-30, y-30, x+30, y+30, outline="black", width=2, fill="light yellow")
            # Draw a circular arrow inside
            self.canvas.create_arc(x-20, y-20, x+20, y+20, start=45, extent=270, 
                                   style="arc", outline="black", width=2, arrow=tk.LAST)
            text_id = self.canvas.create_text(x, y-40, text=component['params']['label'])
        
        elif "Amplifier" in component_name:
            # Draw optical amplifier as a triangle
            obj_id = self.canvas.create_polygon(x-30, y-25, x-30, y+25, x+30, y, 
                                               outline="black", fill="light green", width=2)
            text_id = self.canvas.create_text(x, y-35, text=component['params']['label'])
        
        else:
            # Generic component
            obj_id = self.canvas.create_rectangle(x-30, y-30, x+30, y+30, outline="black")
            text_id = self.canvas.create_text(x, y, text=component['params']['label'])
        
        # Store the canvas objects for later reference
        self.canvas_objects.append({
            'component_index': index,
            'obj_id': obj_id,
            'text_id': text_id
        })
    
    def draw_connections(self):
        """Draw beam connections between components."""
        if len(self.components) < 2:
            return
        
        # Draw straight lines between consecutive components
        for i in range(len(self.components) - 1):
            x1, y1 = self.components[i]['position']
            x2, y2 = self.components[i+1]['position']
            
            # Create a beam line with proper tagging for redrawing
            self.canvas.create_line(
                x1, y1, x2, y2, 
                fill="red", 
                width=2, 
                dash=(4, 2),
                tags="connection"
            )
    
    def on_mouse_down(self, event):
        """Handle mouse button press on the canvas."""
        # Check if clicked on any component
        for obj in self.canvas_objects:
            item = obj['obj_id']
            bbox = self.canvas.bbox(item)
            if bbox and bbox[0] <= event.x <= bbox[2] and bbox[1] <= event.y <= bbox[3]:
                self.selected_item = obj
                self.drag_start_x = event.x
                self.drag_start_y = event.y
                break
    
    def on_mouse_drag(self, event):
        """Handle mouse drag on the canvas."""
        if self.selected_item:
            # Calculate movement delta
            dx = event.x - self.drag_start_x
            dy = event.y - self.drag_start_y
            
            # Move the component and its label
            self.canvas.move(self.selected_item['obj_id'], dx, dy)
            self.canvas.move(self.selected_item['text_id'], dx, dy)
            
            # Update tracking position
            self.drag_start_x = event.x
            self.drag_start_y = event.y
            
            # Update component position in the data structure
            component_index = self.selected_item['component_index']
            x, y = self.components[component_index]['position']
            self.components[component_index]['position'] = (x + dx, y + dy)
            
            # Redraw connections
            self.canvas.delete("connection")
            self.draw_connections()
    
    def on_mouse_up(self, event):
        """Handle mouse button release on the canvas."""
        self.selected_item = None 