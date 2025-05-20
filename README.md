# Laser Components Canvas

An interactive canvas application for designing laser optics experiments using the ComponentLibrary vector graphics by Alexander Franzen.

## Features

- **Component Library**: Browse and search through a comprehensive library of laser optics components
- **Drag and Drop Interface**: Easily place components on the canvas
- **Resizable Components**: Adjust the size of components as needed
- **Text Labels**: Add custom text labels to annotate your design
- **Connection Lines**: Connect components with lines to show the path of light
- **Save and Load Layouts**: Save your designs and load them later
- **Database Integration**: Components from the database are available for easy access

## Getting Started

1. **Installation**:
   ```bash
   npm install
   npm start
   ```

2. **Using the Canvas**:
   - The application has two tabs: "Data Grid" and "Canvas Editor"
   - In the "Data Grid" tab, you can view and edit the component database
   - In the "Canvas Editor" tab, you can create your laser optics designs

## Canvas Editor Usage

### Component Library

- **Browse Components**: Scroll through the component library to find the components you need
- **Search Components**: Use the search bar to find specific components
- **Filter by Category**: Use the category buttons to filter components by type:
  - **Beam**: Optical components for beam control
  - **Complex**: More complex optical systems
  - **Electronic**: Electronic components

### Adding Components to Canvas

- **From Library**: Click on any component in the library to add it to the canvas
- **From Database**: Click on any component in the database list to add it to the canvas
- **Text Labels**: Click the "Add Label" button to add a text label to the canvas

### Manipulating Components

- **Move**: Click and drag components to position them on the canvas
- **Resize**: Drag the resize handle (bottom-right corner) to resize components
- **Delete**: Hover over a component and click the "×" button, or select a component and press Delete
- **Edit Text Labels**: Double-click on a text label to edit its content

### Connecting Components

- Connect components by clicking and dragging from one connection point to another

### Managing Layouts

- **Save Layout**: Click "Save Layout" to save your current design
- **Load Layout**: Click on a saved layout name to load it
- **Delete Layout**: Click the "×" button next to a saved layout to delete it
- **Clear Canvas**: Click "Clear Canvas" to remove all components from the canvas

## Component Library

The component library is based on the ComponentLibrary vector graphics by Alexander Franzen (2006), available at [http://www.gwoptics.org/component_library/](http://www.gwoptics.org/component_library/).

## License

The ComponentLibrary by Alexander Franzen is licensed under a Creative Commons Attribution-NonCommercial 3.0 Unported License.

This application is for educational and research purposes only. 