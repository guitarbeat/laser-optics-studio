# Optical Components Reference Guide

This document provides a reference for the optical components available in the pst-optexp package, along with their parameters and usage examples.

## Basic Components

### Light Sources

| Component | LaTeX Command | Key Parameters | Description |
|-----------|--------------|----------------|-------------|
| Laser Source | `\optbox[position=start]` | wavelength, label | A laser light source |
| LED Source | `\optbox[position=start]` | wavelength, label | An LED light source |
| SLED Source | `\optbox[position=start]` | wavelength, label | A superluminescent LED source |
| Seed Laser | `\optbox[position=start]` | wavelength, label | A seed laser for amplification |

### Optical Elements

| Component | LaTeX Command | Key Parameters | Description |
|-----------|--------------|----------------|-------------|
| Lens | `\lens` | lensradius, focallength | Focusing/collimating element |
| Mirror | `\mirror` | mirrorradius, angle | Reflective surface for beam redirection |
| Beam Splitter | `\beamsplitter` | bssize, splitratio | Splits beam into two paths |
| Polarizing Beam Splitter | `\beamsplitter` | bssize, splitratio | Splits beam based on polarization |
| Half-Wave Plate | `\optretplate` | platesize | Rotates polarization by 90° |
| Quarter-Wave Plate | `\optretplate` | platesize, retardance=quarter | Converts linear to circular polarization |
| Dichroic Mirror | `\beamsplitter` | bssize | Wavelength-selective beam splitter |
| Grating | `\optgrating` | gratingwidth, gratingheight | Diffracts light by wavelength |
| EOM | `\eom` | eomheight, eomlength | Electro-optic modulator |
| AOM | `\aom` | aomheight, aomangle | Acousto-optic modulator |
| Fiber | `\optfiber` | fiberloopradius, fiberloopangle | Optical fiber |
| Beam Block | `\optdetector[dettype=block]` | detsize | Absorbs/blocks beam |

### Detectors

| Component | LaTeX Command | Key Parameters | Description |
|-----------|--------------|----------------|-------------|
| Photodiode | `\optbox[position=end]` | label | General light detector |
| Photomultiplier Tube | `\optbox[position=end]` | label | PMT detector for low-light detection |
| Camera | `\optbox[position=end]` | label | Image detector |
| Power Meter | `\optbox[position=end]` | label | Measures optical power |
| Spectrometer | `\optbox[position=end]` | label | Measures spectral content |

## Advanced Components

### Scientific Components

| Component | LaTeX Command | Key Parameters | Description |
|-----------|--------------|----------------|-------------|
| Objective Lens | `\lens` | lensradius, focallength, label="OBJ" | Microscope objective |
| Collection Optics | `\optbox` | optboxwidth, label="CO" | Light collection system |
| Galvo Scanners | `\optbox` | optboxwidth, label="GG" | Galvanometer scanner system |
| Pulse Gating System | `\optbox` | optboxwidth | Optical pulse selection system |
| D-Shaped Mirror | `\mirror[mirrortype=extended]` | angle | Specialized mirror shape |
| Grating Compressor | `\optbox` | optboxwidth | Pulse compression system |

### Special Elements

| Component | LaTeX Command | Key Parameters | Description |
|-----------|--------------|----------------|-------------|
| Optical Isolator | `\optisolator` | isolatorsize | Prevents backward reflections |
| Optical Circulator | `\optcirculator` | circulatorradius | Directs light between ports |
| Optical Amplifier | `\optamplifier` | ampwidth, amplength | Amplifies optical signal |
| Wavelength Division Multiplexer | `\optbox` | label="WDM" | Combines multiple wavelengths |
| Polarization Controller | `\optbox` | label="PC" | Manipulates polarization state |

## Component Parameters

### Global Parameters

These parameters apply to most components:

| Parameter | Description | Default | Example |
|-----------|-------------|---------|---------|
| label | Text displayed with component | Component name | "Lens L1" |
| labeloffset | Distance of label from component | 0.3 | labeloffset=0.5 |
| labelangle | Angle of label placement | :U (above) | labelangle=:D (below) |

### Beam Parameters

To customize beam appearance:

```latex
\addtopsstyle{Beam}{linestyle=none, fillstyle=solid, fillcolor=red}
\drawwidebeam[beamwidth=0.1]{1-4}
```

Available colors: red, green, blue, cyan, magenta, yellow, etc.

## Usage Examples

### Basic Lens System

```latex
\begin{pspicture}(-1,-1)(12,6)
    % Node definitions
    \pnodes(1,4){Source}(4,4){Lens1}(8,4){Lens2}(11,4){Image}
    
    \begin{optexp}
        \optbox[position=start, innerlabel, optboxwidth=1.2](Source)(Lens1){Light Source}
        \lens[lensradius=1.2](Lens1)(Lens2){Lens 1}
        \lens[lensradius=0.8](Lens2)(Image){Lens 2}
        \optbox[position=end, innerlabel, optboxwidth=1.2](Image)(Image){Image}
        
        % Beam
        \addtopsstyle{Beam}{linestyle=none, fillstyle=solid, fillcolor=green!70!black}
        \drawwidebeam[beamwidth=0.15]{1-4}
    \end{optexp}
\end{pspicture}
```

### Michelson Interferometer

```latex
\begin{pspicture}(-2,-3)(8,3)
    % Node definitions
    \pnodes(0,0){Source}(3,0){BS}(3,2){M1}(6,0){M2}(3,-2){Det}
    
    \begin{optexp}
        % Components
        \optbox[position=start, innerlabel](Source)(BS){Laser}
        \beamsplitter(BS)(M1)(M2){BS}
        \mirror(BS)(M1){M1}
        \mirror(BS)(M2){M2}
        \optbox[position=end, innerlabel](BS)(Det){Detector}
        
        % Beams
        \addtopsstyle{Beam}{linestyle=none, fillstyle=solid, fillcolor=red}
        \drawwidebeam[beamwidth=0.1]{1-2}
        \drawwidebeam[beamwidth=0.1]{2-3}
        \drawwidebeam[beamwidth=0.1]{2-4}
        \drawwidebeam[beamwidth=0.1]{2-5}
    \end{optexp}
\end{pspicture}
```

## Tips for Professional Diagrams

1. **Consistent Spacing**: Maintain consistent spacing between components
2. **Proper Scaling**: Use appropriate sizes for different components
3. **Color Coding**: Use different colors for different wavelengths or beam paths
4. **Clear Labels**: Label all important components, but avoid cluttering
5. **Beam Width**: Use beam width to indicate focusing/diverging beams
6. **Grouping**: Group related components together visually
7. **Annotations**: Add annotations for key measurements or parameters

## LaTeX Tips

- Use the `standalone` document class for easy embedding in other documents
- For complex diagrams, define nodes with meaningful names
- Add a title or caption using `\rput[b](x,y){Title}`
- Customize colors with the `xcolor` package (e.g., `red!70!black` for a darker red)