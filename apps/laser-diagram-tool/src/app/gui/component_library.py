"""
ComponentLibrary - Manages the available optical components
"""

class ComponentLibrary:
    """Class to manage the optical component library."""
    
    def __init__(self):
        """Initialize the component library with default components."""
        # Component library - defined as tuples (display_name, LaTeX command, params)
        self.components = {
            "Light Sources": [
                ("Laser Source", "\\optbox[position=start, innerlabel, optboxwidth=1.2]", 
                {"wavelength": "1064", "label": "Laser"}),
                ("LED Source", "\\optbox[position=start, innerlabel, optboxwidth=1.2]", 
                {"wavelength": "650", "label": "LED"}),
                ("SLED Source", "\\optbox[position=start, innerlabel, optboxwidth=1.2]", 
                {"wavelength": "850", "label": "SLED"}),
                ("Seed Laser", "\\optbox[position=start, innerlabel, optboxwidth=1.2]", 
                {"wavelength": "1550", "label": "Seed"})
            ],
            "Optical Components": [
                ("Lens", "\\lens[lensradius=1]", {"label": "Lens", "focal_length": "50"}),
                ("Thick Lens", "\\lens[lensradius=1, lenstype=thick]", {"label": "Thick Lens", "focal_length": "50"}),
                ("Mirror", "\\mirror[mirrortype=extended]", {"label": "Mirror", "angle": "45"}),
                ("Curved Mirror", "\\mirror[mirrortype=curved]", {"label": "CM", "angle": "45", "radius": "30"}),
                ("Beam Splitter", "\\beamsplitter[bsstyle=plate]", {"label": "BS", "ratio": "50:50"}),
                ("Polarizing Beam Splitter", "\\beamsplitter[bsstyle=cube]", {"label": "PBS", "ratio": "50:50"}),
                ("Half-Wave Plate", "\\optretplate[platetype=half]", {"label": "HWP"}),
                ("Quarter-Wave Plate", "\\optretplate[platetype=quarter]", {"label": "QWP"}),
                ("Optical Isolator", "\\optisolator", {"label": "Isolator"}),
                ("Grating", "\\optgrating", {"label": "Grating", "gratingwidth": "1.5"}),
                ("Fiber", "\\optfiber[fibertype=patch]", {"label": "Fiber"})
            ],
            "Modulators & Filters": [
                ("Acoustic-Optic Modulator", "\\aom", {"label": "AOM"}),
                ("Electro-Optic Modulator", "\\eom", {"label": "EOM"}),
                ("Bandpass Filter", "\\optfilter[filtertype=bandpass]", {"label": "BPF"}),
                ("Neutral Density Filter", "\\optfilter[filtertype=nd]", {"label": "ND"})
            ],
            "Detectors": [
                ("Photodiode", "\\optbox[position=end, innerlabel, optboxwidth=1.2]", 
                {"label": "PD"}),
                ("Camera", "\\optbox[position=end, innerlabel, optboxwidth=1.2]", 
                {"label": "Camera"}),
                ("Power Meter", "\\optbox[position=end, innerlabel, optboxwidth=1.2]", 
                {"label": "Pwr Meter"}),
                ("Spectrometer", "\\optbox[position=end, innerlabel, optboxwidth=1.2]", 
                {"label": "Spec"}),
                ("Beam Block", "\\optdetector[dettype=block]", {"label": "Block"})
            ],
            "Scientific Components": [
                ("Objective Lens", "\\lens[lensradius=1.2, lenstype=objective]", {"label": "OBJ", "focal_length": "4"}),
                ("Collection Optics", "\\optbox[innerlabel, optboxwidth=1.5]", {"label": "CO"}),
                ("Galvo Scanners", "\\optbox[innerlabel, optboxwidth=1.5]", {"label": "Galvo"}),
                ("Optical Circulator", "\\optcirculator", {"label": "Circ"}),
                ("Optical Amplifier", "\\optamplifier", {"label": "Amp"}),
                ("Wavelength Division Multiplexer", "\\optbox[innerlabel, optboxwidth=1.8]", {"label": "WDM"})
            ],
            "Quantum Optics": [
                ("Single Photon Source", "\\optbox[position=start, innerlabel, optboxwidth=1.5]", {"label": "SPS"}),
                ("Entangled Photon Source", "\\optbox[position=start, innerlabel, optboxwidth=1.8]", {"label": "EPS"}),
                ("Single Photon Detector", "\\optbox[position=end, innerlabel, optboxwidth=1.5]", {"label": "SPD"}),
                ("Bell State Analyzer", "\\optbox[innerlabel, optboxwidth=1.8]", {"label": "BSA"}),
                ("Photon Number Counter", "\\optbox[position=end, innerlabel, optboxwidth=1.8]", {"label": "PNC"})
            ],
            "Optical Setups": [
                # Common interferometers and optical setups
                # These are complex components that would be expanded into multiple components
                # when added to the diagram
                ("Michelson Interferometer", "michelson_interferometer", {
                    "label": "Michelson",
                    "components": [
                        {"type": "Laser Source", "position": (100, 200), "params": {"label": "Laser"}},
                        {"type": "Beam Splitter", "position": (250, 200), "params": {"label": "BS"}},
                        {"type": "Mirror", "position": (400, 200), "params": {"label": "M1"}},
                        {"type": "Mirror", "position": (250, 350), "params": {"label": "M2"}},
                        {"type": "Detector", "position": (100, 350), "params": {"label": "Det"}}
                    ],
                    "beams": [
                        {"start": 0, "end": 1, "type": "wide"},
                        {"start": 1, "end": 2, "type": "wide"},
                        {"start": 1, "end": 3, "type": "wide"},
                        {"start": 1, "end": 4, "type": "wide"}
                    ]
                }),
                ("Mach-Zehnder Interferometer", "mach_zehnder_interferometer", {
                    "label": "MZI",
                    "components": [
                        {"type": "Laser Source", "position": (100, 200), "params": {"label": "Laser"}},
                        {"type": "Beam Splitter", "position": (250, 200), "params": {"label": "BS1"}},
                        {"type": "Mirror", "position": (400, 150), "params": {"label": "M1"}},
                        {"type": "Mirror", "position": (400, 250), "params": {"label": "M2"}},
                        {"type": "Beam Splitter", "position": (550, 200), "params": {"label": "BS2"}},
                        {"type": "Detector", "position": (700, 200), "params": {"label": "Det"}}
                    ],
                    "beams": [
                        {"start": 0, "end": 1, "type": "wide"},
                        {"start": 1, "end": 2, "type": "wide"},
                        {"start": 1, "end": 3, "type": "wide"},
                        {"start": 2, "end": 4, "type": "wide"},
                        {"start": 3, "end": 4, "type": "wide"},
                        {"start": 4, "end": 5, "type": "wide"}
                    ]
                }),
                ("Fabry-Perot Cavity", "fabry_perot_cavity", {
                    "label": "FP Cavity",
                    "components": [
                        {"type": "Laser Source", "position": (100, 200), "params": {"label": "Laser"}},
                        {"type": "Mirror", "position": (250, 200), "params": {"label": "M1"}},
                        {"type": "Mirror", "position": (450, 200), "params": {"label": "M2"}},
                        {"type": "Detector", "position": (600, 200), "params": {"label": "Det"}}
                    ],
                    "beams": [
                        {"start": 0, "end": 1, "type": "wide"},
                        {"start": 1, "end": 2, "type": "resizable"},
                        {"start": 2, "end": 3, "type": "wide"}
                    ]
                }),
                ("Ring Cavity", "ring_cavity", {
                    "label": "Ring Cavity",
                    "components": [
                        {"type": "Laser Source", "position": (100, 200), "params": {"label": "Laser"}},
                        {"type": "Mirror", "position": (250, 200), "params": {"label": "M1"}},
                        {"type": "Mirror", "position": (400, 100), "params": {"label": "M2"}},
                        {"type": "Mirror", "position": (550, 200), "params": {"label": "M3"}},
                        {"type": "Mirror", "position": (400, 300), "params": {"label": "M4"}},
                        {"type": "Detector", "position": (700, 200), "params": {"label": "Det"}}
                    ],
                    "beams": [
                        {"start": 0, "end": 1, "type": "wide"},
                        {"start": 1, "end": 2, "type": "wide"},
                        {"start": 2, "end": 3, "type": "wide"},
                        {"start": 3, "end": 4, "type": "wide"},
                        {"start": 4, "end": 1, "type": "wide"},
                        {"start": 3, "end": 5, "type": "wide"}
                    ]
                }),
                ("Fiber Optic Link", "fiber_optic_link", {
                    "label": "Fiber Link",
                    "components": [
                        {"type": "Laser Source", "position": (100, 200), "params": {"label": "Laser"}},
                        {"type": "Lens", "position": (200, 200), "params": {"label": "L1"}},
                        {"type": "Fiber", "position": (350, 200), "params": {"label": "Fiber"}},
                        {"type": "Lens", "position": (500, 200), "params": {"label": "L2"}},
                        {"type": "Detector", "position": (600, 200), "params": {"label": "Det"}}
                    ],
                    "beams": [
                        {"start": 0, "end": 1, "type": "wide"},
                        {"start": 1, "end": 2, "type": "resizable"},
                        {"start": 2, "end": 3, "type": "narrow"},
                        {"start": 3, "end": 4, "type": "resizable"}
                    ]
                })
            ]
        }
    
    def load_components_to_tree(self, tree):
        """Load available components into the tree view."""
        tree.delete(*tree.get_children())
        
        for category, components in self.components.items():
            category_id = tree.insert("", "end", text=category)
            for component in components:
                name = component[0]
                tree.insert(category_id, "end", text=name, values=(name,))
    
    def get_component_by_name(self, name):
        """Find a component by its display name."""
        for category, components in self.components.items():
            for component in components:
                if component[0] == name:
                    return component
        return None
    
    def get_all_components(self):
        """Return all components as a flat list."""
        all_components = []
        for category, components in self.components.items():
            all_components.extend(components)
        return all_components
    
    def is_complex_setup(self, component_name):
        """Check if the component is a complex optical setup."""
        component = self.get_component_by_name(component_name)
        if component and component[1] in [
            'michelson_interferometer',
            'mach_zehnder_interferometer',
            'fabry_perot_cavity',
            'ring_cavity',
            'fiber_optic_link'
        ]:
            return True
        return False
    
    def get_setup_components(self, setup_name):
        """Get the components and beams for a complex optical setup."""
        component = self.get_component_by_name(setup_name)
        if component and 'components' in component[2]:
            return component[2]['components'], component[2].get('beams', [])
        return [], [] 