"""
Diagram - Model for optical diagrams
"""

import json
import os
from app.models.optical_component import OpticalComponent

class Diagram:
    """Class representing an optical diagram."""
    
    def __init__(self, name="Untitled Diagram"):
        """Initialize a new diagram."""
        self.name = name
        self.components = []
        self.file_path = None
    
    def add_component(self, component):
        """Add a component to the diagram."""
        if isinstance(component, OpticalComponent):
            self.components.append(component)
        elif isinstance(component, dict):
            self.components.append(OpticalComponent.from_dict(component))
        else:
            raise TypeError("Component must be an OpticalComponent or dict")
    
    def remove_component(self, index):
        """Remove a component from the diagram."""
        if 0 <= index < len(self.components):
            del self.components[index]
    
    def clear(self):
        """Clear all components from the diagram."""
        self.components = []
    
    def save(self, file_path=None):
        """Save the diagram to a file."""
        if file_path:
            self.file_path = file_path
        elif not self.file_path:
            raise ValueError("No file path specified")
        
        # Convert components to dictionaries
        component_dicts = [comp.to_dict() for comp in self.components]
        
        # Create the diagram data
        diagram_data = {
            'name': self.name,
            'components': component_dicts
        }
        
        # Write to file
        with open(self.file_path, 'w') as f:
            json.dump(diagram_data, f, indent=2)
    
    @classmethod
    def load(cls, file_path):
        """Load a diagram from a file."""
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Create a new diagram
        diagram = cls(data.get('name', 'Untitled Diagram'))
        diagram.file_path = file_path
        
        # Add components
        for comp_data in data.get('components', []):
            diagram.add_component(comp_data)
        
        return diagram
    
    def get_component_dicts(self):
        """Get all components as dictionaries."""
        return [comp.to_dict() for comp in self.components] 