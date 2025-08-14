"""
OpticalComponent - Models for optical components and their properties
"""

class OpticalComponent:
    """Base class for all optical components."""
    
    def __init__(self, name, latex_cmd, params, position=(0, 0)):
        """Initialize an optical component."""
        self.name = name
        self.latex_cmd = latex_cmd
        self.params = params
        self.position = position
    
    def to_dict(self):
        """Convert to dictionary representation."""
        return {
            'name': self.name,
            'latex': self.latex_cmd,
            'params': self.params,
            'position': self.position
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create an OpticalComponent from a dictionary."""
        return cls(
            data['name'],
            data['latex'],
            data['params'],
            data['position']
        )


class LightSource(OpticalComponent):
    """Class representing light sources like lasers and LEDs."""
    
    def __init__(self, name, wavelength, label, position=(0, 0)):
        """Initialize a light source."""
        latex_cmd = "\\optbox[position=start, innerlabel, optboxwidth=1.2]"
        params = {
            'wavelength': str(wavelength),
            'label': label
        }
        super().__init__(name, latex_cmd, params, position)


class Lens(OpticalComponent):
    """Class representing optical lenses."""
    
    def __init__(self, label, focal_length, position=(0, 0)):
        """Initialize a lens."""
        latex_cmd = "\\lens"
        params = {
            'label': label,
            'focal_length': str(focal_length)
        }
        super().__init__("Lens", latex_cmd, params, position)


class Mirror(OpticalComponent):
    """Class representing mirrors."""
    
    def __init__(self, label, angle=45, position=(0, 0)):
        """Initialize a mirror."""
        latex_cmd = "\\mirror"
        params = {
            'label': label,
            'angle': str(angle)
        }
        super().__init__("Mirror", latex_cmd, params, position)


class Detector(OpticalComponent):
    """Class representing optical detectors."""
    
    def __init__(self, name, label, position=(0, 0)):
        """Initialize a detector."""
        latex_cmd = "\\optbox[position=end, innerlabel, optboxwidth=1.2]"
        params = {
            'label': label
        }
        super().__init__(name, latex_cmd, params, position) 