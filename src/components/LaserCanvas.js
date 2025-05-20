import React, { useState, useEffect, useCallback } from "react";
import { ResizableBox } from "react-resizable";
import ReactFlow, {
  addEdge,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  Handle,
  Position,
  MarkerType,
} from "react-flow-renderer";
import "react-resizable/css/styles.css";
import "./LaserCanvas.css";

// Component categories
const componentCategories = {
  "Beam Control (b-)": ["b-"],
  "Complex Components (c-)": ["c-"],
  "Electronic Components (e-)": ["e-"],
};

// Component node for React Flow
const ComponentNode = ({ data }) => {
  return (
    <ResizableBox
      width={data.width || 100}
      height={data.height || 100}
      minConstraints={[50, 50]}
      maxConstraints={[300, 300]}
      onResizeStop={(e, { size }) => {
        if (data.onResize) {
          data.onResize(size);
        }
      }}
      className="component-resizable-box"
    >
      <div className="component-node">
        <div className="delete-node" onClick={data.onDelete}>×</div>
        <img 
          src={data.svgPath} 
          alt={data.label} 
          className="component-svg"
        />
        <div className="component-label">{data.label}</div>
        <Handle
          type="target"
          position={Position.Left}
          id="left"
          style={{ background: '#ff5252', width: 8, height: 8 }}
        />
        <Handle
          type="source"
          position={Position.Right}
          id="right"
          style={{ background: '#ff5252', width: 8, height: 8 }}
        />
        <Handle
          type="target"
          position={Position.Top}
          id="top"
          style={{ background: '#ff5252', width: 8, height: 8 }}
        />
        <Handle
          type="source"
          position={Position.Bottom}
          id="bottom"
          style={{ background: '#ff5252', width: 8, height: 8 }}
        />
      </div>
    </ResizableBox>
  );
};

// Text Label Node
const TextLabelNode = ({ data }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [text, setText] = useState(data.text || "Text Label");
  
  const handleDoubleClick = () => {
    setIsEditing(true);
  };
  
  const handleBlur = () => {
    setIsEditing(false);
    if (data.onTextChange) {
      data.onTextChange(text);
    }
  };
  
  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      setIsEditing(false);
      if (data.onTextChange) {
        data.onTextChange(text);
      }
    }
  };
  
  return (
    <ResizableBox
      width={data.width || 150}
      height={data.height || 50}
      minConstraints={[50, 30]}
      maxConstraints={[500, 200]}
      onResizeStop={(e, { size }) => {
        if (data.onResize) {
          data.onResize(size);
        }
      }}
      className="text-label-resizable-box"
    >
      <div className="text-label-node">
        <div className="delete-node" onClick={data.onDelete}>×</div>
        {isEditing ? (
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            onBlur={handleBlur}
            onKeyDown={handleKeyDown}
            className="text-label-input"
            autoFocus
          />
        ) : (
          <div 
            className="text-label-content" 
            onDoubleClick={handleDoubleClick}
            style={{ fontSize: data.fontSize || '14px' }}
          >
            {text}
          </div>
        )}
      </div>
    </ResizableBox>
  );
};

// Custom node types
const nodeTypes = {
  componentNode: ComponentNode,
  textLabelNode: TextLabelNode,
};

function LaserCanvas() {
  const [components, setComponents] = useState([]);
  const [libraryComponents, setLibraryComponents] = useState([]);
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selectedComponent, setSelectedComponent] = useState(null);
  const [activeCategory, setActiveCategory] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");
  const [savedLayouts, setSavedLayouts] = useState([]);
  const [layoutName, setLayoutName] = useState("");
  const [showSaveDialog, setShowSaveDialog] = useState(false);
  const [labelText, setLabelText] = useState("New Label");
  const [labelFontSize, setLabelFontSize] = useState("14px");
  const [showLabelDialog, setShowLabelDialog] = useState(false);
  const [showDatabaseComponents, setShowDatabaseComponents] = useState(false);
  const [beamType, setBeamType] = useState("red");
  
  // Load component data from CSV
  useEffect(() => {
    fetch('/data.csv')
      .then(response => response.text())
      .then(csvData => {
        const lines = csvData.split('\n');
        const headers = lines[0].split(',');
        
        const parsedData = lines.slice(1).filter(line => line.trim()).map(line => {
          const values = line.split(',');
          const component = {};
          
          headers.forEach((header, index) => {
            component[header] = values[index];
          });
          
          return component;
        });
        
        setComponents(parsedData);
      })
      .catch(error => console.error('Error loading component data:', error));
      
    // Load all SVG components from the library
    fetch('/ComponentLibrary_files/svg')
      .then(response => {
        // If we can't directly list the directory, we'll use a predefined list
        const svgFiles = [
          "b-bsp.svg", "b-bspcube.svg", "b-coupler.svg", "b-credit.svg", "b-crystalcc.svg",
          "b-crystalfc.svg", "b-crystalff.svg", "b-diccube.svg", "b-dicgrn.svg", "b-dicred.svg",
          "b-dump.svg", "b-grat.svg", "b-lens1.svg", "b-lens2.svg", "b-lens3.svg",
          "b-mir.svg", "b-mirc.svg", "b-mircpzt.svg", "b-mirpzt.svg", "b-npro.svg",
          "b-phase.svg", "b-wpgn.svg", "b-wpred.svg", "b-wpyel.svg",
          "c-aom.svg", "c-diodegrn.svg", "c-eom1.svg", "c-eom2.svg", "c-fiber.svg",
          "c-fibercoupl.svg", "c-flip.svg", "c-isolator.svg", "c-laser1.svg", "c-laser2.svg",
          "c-mirpzt3ax.svg", "c-modeclean.svg", "c-modecleanpzt.svg", "c-opacc.svg",
          "c-opaccplates.svg", "c-opacfplates.svg", "c-opafc.svg", "c-opaff.svg",
          "c-opaffplates.svg", "c-opakerr.svg", "c-opared.svg", "c-rotator.svg",
          "e-amp.svg", "e-computer.svg", "e-diff.svg", "e-frq1.svg", "e-frq2.svg",
          "e-hipass.svg", "e-hvampleft.svg", "e-hvampright.svg", "e-lopass.svg", "e-mix.svg",
          "e-pd1.svg", "e-pd2.svg", "e-pdgrn1.svg", "e-pdgrn2.svg", "e-qpd.svg",
          "e-servoleft.svg", "e-servoright.svg", "e-spekki.svg", "e-sum.svg", "e-sumdiff.svg"
        ];
        
        const libraryItems = svgFiles.map(file => {
          const name = file.replace('.svg', '');
          const prettyName = name
            .split('-')
            .slice(1)
            .join('-')
            .toUpperCase();
          
          return {
            id: name,
            name: prettyName,
            category: name.substring(0, 2),
            path: `/ComponentLibrary_files/svg/${file}`
          };
        });
        
        setLibraryComponents(libraryItems);
      })
      .catch(error => {
        console.error('Error loading library components:', error);
      });
      
    // Load saved layouts from localStorage
    const savedLayoutsData = localStorage.getItem('laser-canvas-layouts');
    if (savedLayoutsData) {
      try {
        setSavedLayouts(JSON.parse(savedLayoutsData));
      } catch (error) {
        console.error('Error loading saved layouts:', error);
      }
    }
    
    // Add keyboard shortcut for delete
    const handleKeyDown = (event) => {
      if ((event.key === 'Delete' || event.key === 'Backspace') && selectedComponent) {
        deleteNode(selectedComponent.id);
        setSelectedComponent(null);
      }
    };
    
    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [selectedComponent]);

  const addComponentToCanvas = (component, svgPath) => {
    const id = `component-${Date.now()}`;
    const position = { x: Math.random() * 300, y: Math.random() * 300 };
    
    const newNode = {
      id,
      type: "componentNode",
      position,
      data: {
        label: component.name || component.Element,
        system: component.System,
        model: component.Model,
        svgPath: svgPath || component.path,
        width: 120,
        height: 120,
        onResize: (size) => {
          setNodes((nds) =>
            nds.map((node) => {
              if (node.id === id) {
                return {
                  ...node,
                  data: {
                    ...node.data,
                    width: size.width,
                    height: size.height,
                  },
                };
              }
              return node;
            })
          );
        },
        onDelete: () => deleteNode(id),
      },
      draggable: true,
    };

    setNodes((nds) => [...nds, newNode]);
  };
  
  // Add text label to canvas
  const addTextLabel = () => {
    const id = `text-${Date.now()}`;
    const position = { x: Math.random() * 300, y: Math.random() * 300 };
    
    const newNode = {
      id,
      type: "textLabelNode",
      position,
      data: {
        text: labelText,
        fontSize: labelFontSize,
        width: 150,
        height: 50,
        onResize: (size) => {
          setNodes((nds) =>
            nds.map((node) => {
              if (node.id === id) {
                return {
                  ...node,
                  data: {
                    ...node.data,
                    width: size.width,
                    height: size.height,
                  },
                };
              }
              return node;
            })
          );
        },
        onTextChange: (newText) => {
          setNodes((nds) =>
            nds.map((node) => {
              if (node.id === id) {
                return {
                  ...node,
                  data: {
                    ...node.data,
                    text: newText,
                  },
                };
              }
              return node;
            })
          );
        },
        onDelete: () => deleteNode(id),
      },
      draggable: true,
    };
    
    setNodes((nds) => [...nds, newNode]);
    setShowLabelDialog(false);
    setLabelText("New Label");
  };

  const onConnect = useCallback((params) => {
    // Create edge with selected beam type and appropriate styling
    const newEdge = {
      ...params,
      type: 'smoothstep',
      animated: true,
      style: { stroke: getBeamColor(), strokeWidth: 2 },
      markerEnd: {
        type: MarkerType.ArrowClosed,
        color: getBeamColor(),
      },
    };
    setEdges((eds) => addEdge(newEdge, eds));
  }, [beamType]);

  const onNodeClick = (event, node) => {
    setSelectedComponent(node);
  };
  
  // Delete a node
  const deleteNode = useCallback((id) => {
    setNodes((nds) => nds.filter((node) => node.id !== id));
    setEdges((eds) => eds.filter((edge) => edge.source !== id && edge.target !== id));
  }, [setNodes, setEdges]);

  // Filter library components based on category and search term
  const filteredLibraryComponents = libraryComponents.filter(component => {
    const matchesCategory = activeCategory === "all" || component.category === activeCategory;
    const matchesSearch = component.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
                         component.id.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesCategory && matchesSearch;
  });
  
  // Get beam color based on selected type
  const getBeamColor = () => {
    switch(beamType) {
      case 'red': return '#ff0000';
      case 'green': return '#00ff00';
      case 'blue': return '#0000ff';
      case 'infrared': return '#ff6666';
      default: return '#ff0000';
    }
  };
  
  // Save current layout
  const saveLayout = useCallback(() => {
    if (!layoutName.trim()) return;
    
    const layout = {
      id: `layout-${Date.now()}`,
      name: layoutName,
      nodes,
      edges,
      date: new Date().toISOString(),
    };
    
    const updatedLayouts = [...savedLayouts, layout];
    setSavedLayouts(updatedLayouts);
    localStorage.setItem('laser-canvas-layouts', JSON.stringify(updatedLayouts));
    
    setLayoutName("");
    setShowSaveDialog(false);
  }, [layoutName, nodes, edges, savedLayouts]);
  
  // Load selected layout
  const loadLayout = useCallback((layout) => {
    setNodes(layout.nodes);
    setEdges(layout.edges);
  }, [setNodes, setEdges]);
  
  // Delete layout
  const deleteLayout = useCallback((layoutId) => {
    const updatedLayouts = savedLayouts.filter(layout => layout.id !== layoutId);
    setSavedLayouts(updatedLayouts);
    localStorage.setItem('laser-canvas-layouts', JSON.stringify(updatedLayouts));
  }, [savedLayouts]);
  
  // Clear canvas
  const clearCanvas = useCallback(() => {
    if (window.confirm('Are you sure you want to clear the canvas?')) {
      setNodes([]);
      setEdges([]);
    }
  }, [setNodes, setEdges]);

  return (
    <div className="laser-canvas-container">
      <div className="sidebar">
        <h3>Component Library</h3>
        
        {/* Search bar */}
        <div className="search-container">
          <input
            type="text"
            placeholder="Search components..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>
        
        {/* Category filters */}
        <div className="category-filters">
          <button 
            className={`category-button ${activeCategory === "all" ? "active" : ""}`}
            onClick={() => setActiveCategory("all")}
          >
            All
          </button>
          <button 
            className={`category-button ${activeCategory === "b-" ? "active" : ""}`}
            onClick={() => setActiveCategory("b-")}
          >
            Beam
          </button>
          <button 
            className={`category-button ${activeCategory === "c-" ? "active" : ""}`}
            onClick={() => setActiveCategory("c-")}
          >
            Complex
          </button>
          <button 
            className={`category-button ${activeCategory === "e-" ? "active" : ""}`}
            onClick={() => setActiveCategory("e-")}
          >
            Electronic
          </button>
        </div>
        
        {/* Component library */}
        <div className="component-library">
          {filteredLibraryComponents.map((component) => (
            <div 
              key={component.id} 
              className="library-component"
              onClick={() => addComponentToCanvas(component)}
            >
              <div className="library-component-preview">
                <img 
                  src={component.path} 
                  alt={component.name} 
                  className="library-component-svg"
                />
              </div>
              <div className="library-component-name">
                {component.name}
              </div>
            </div>
          ))}
        </div>
        
        <hr className="divider" />
        
        {/* Beam Type Selection */}
        <div className="beam-type-selector">
          <h3>Beam Type</h3>
          <div className="beam-options">
            <button 
              className={`beam-option ${beamType === 'red' ? 'active' : ''}`} 
              onClick={() => setBeamType('red')}
              style={{ backgroundColor: '#ff0000' }}
            >
              Red
            </button>
            <button 
              className={`beam-option ${beamType === 'green' ? 'active' : ''}`} 
              onClick={() => setBeamType('green')}
              style={{ backgroundColor: '#00ff00' }}
            >
              Green
            </button>
            <button 
              className={`beam-option ${beamType === 'blue' ? 'active' : ''}`} 
              onClick={() => setBeamType('blue')}
              style={{ backgroundColor: '#0000ff' }}
            >
              Blue
            </button>
            <button 
              className={`beam-option ${beamType === 'infrared' ? 'active' : ''}`} 
              onClick={() => setBeamType('infrared')}
              style={{ backgroundColor: '#ff6666' }}
            >
              IR
            </button>
          </div>
        </div>
        
        <hr className="divider" />
        
        {/* Canvas Actions */}
        <div className="canvas-actions">
          <button 
            className="action-button"
            onClick={() => setShowSaveDialog(true)}
          >
            Save Layout
          </button>
          <button 
            className="action-button"
            onClick={() => setShowLabelDialog(true)}
          >
            Add Label
          </button>
          <button 
            className="action-button danger"
            onClick={clearCanvas}
          >
            Clear Canvas
          </button>
        </div>
        
        {/* Saved Layouts */}
        {savedLayouts.length > 0 && (
          <>
            <h3>Saved Layouts</h3>
            <div className="saved-layouts">
              {savedLayouts.map((layout) => (
                <div key={layout.id} className="saved-layout">
                  <div className="saved-layout-name" onClick={() => loadLayout(layout)}>
                    {layout.name}
                  </div>
                  <button 
                    className="delete-button"
                    onClick={() => deleteLayout(layout.id)}
                  >
                    ×
                  </button>
                </div>
              ))}
            </div>
          </>
        )}
        
        {/* Toggle Database Components */}
        <div className="toggle-container">
          <button 
            className="toggle-button"
            onClick={() => setShowDatabaseComponents(!showDatabaseComponents)}
          >
            {showDatabaseComponents ? 'Hide Database Components' : 'Show Database Components'}
          </button>
        </div>
        
        {/* Database Components (Hidden by default) */}
        {showDatabaseComponents && (
          <>
            <hr className="divider" />
            <h3>Database Components</h3>
            <div className="component-list">
              {components.map((component, index) => (
                <div 
                  key={index} 
                  className="component-item"
                  onClick={() => {
                    // Find appropriate SVG based on component name
                    let svgPath = null;
                    for (const libComp of libraryComponents) {
                      if (component.Element.toLowerCase().includes(libComp.name.toLowerCase()) || 
                          libComp.name.toLowerCase().includes(component.Element.toLowerCase())) {
                        svgPath = libComp.path;
                        break;
                      }
                    }
                    
                    // Use default if no match found
                    if (!svgPath) {
                      if (component.System === "Laser") {
                        svgPath = "/ComponentLibrary_files/svg/c-laser1.svg";
                      } else if (component.Element.includes("Lens")) {
                        svgPath = "/ComponentLibrary_files/svg/b-lens1.svg";
                      } else if (component.Element.includes("Mirror")) {
                        svgPath = "/ComponentLibrary_files/svg/b-mir.svg";
                      } else {
                        svgPath = "/ComponentLibrary_files/svg/e-computer.svg";
                      }
                    }
                    
                    addComponentToCanvas(component, svgPath);
                  }}
                >
                  {component.Element}
                  {component.Model && <span className="model-info">({component.Model})</span>}
                </div>
              ))}
            </div>
          </>
        )}
      </div>
      <div className="canvas">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onNodeClick={onNodeClick}
          nodeTypes={nodeTypes}
          fitView
        >
          <Background />
          <Controls />
          <MiniMap />
        </ReactFlow>
      </div>
      {selectedComponent && (
        <div className="component-details">
          <h4>{selectedComponent.data.label || selectedComponent.data.text}</h4>
          {selectedComponent.data.system && <p>System: {selectedComponent.data.system}</p>}
          {selectedComponent.data.model && <p>Model: {selectedComponent.data.model}</p>}
          <div className="component-actions">
            <button onClick={() => setSelectedComponent(null)}>Close</button>
            <button 
              className="danger-button"
              onClick={() => {
                deleteNode(selectedComponent.id);
                setSelectedComponent(null);
              }}
            >
              Delete
            </button>
          </div>
        </div>
      )}
      
      {/* Save Layout Dialog */}
      {showSaveDialog && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3>Save Layout</h3>
            <input
              type="text"
              placeholder="Layout name"
              value={layoutName}
              onChange={(e) => setLayoutName(e.target.value)}
              className="layout-name-input"
            />
            <div className="modal-actions">
              <button onClick={() => setShowSaveDialog(false)}>Cancel</button>
              <button 
                onClick={saveLayout}
                disabled={!layoutName.trim()}
                className="primary-button"
              >
                Save
              </button>
            </div>
          </div>
        </div>
      )}
      
      {/* Add Text Label Dialog */}
      {showLabelDialog && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3>Add Text Label</h3>
            <textarea
              placeholder="Enter label text"
              value={labelText}
              onChange={(e) => setLabelText(e.target.value)}
              className="label-text-input"
              rows={3}
            />
            <div className="font-size-control">
              <label>Font Size:</label>
              <select 
                value={labelFontSize} 
                onChange={(e) => setLabelFontSize(e.target.value)}
                className="font-size-select"
              >
                <option value="10px">Small</option>
                <option value="14px">Medium</option>
                <option value="18px">Large</option>
                <option value="24px">Extra Large</option>
              </select>
            </div>
            <div className="modal-actions">
              <button onClick={() => setShowLabelDialog(false)}>Cancel</button>
              <button 
                onClick={addTextLabel}
                disabled={!labelText.trim()}
                className="primary-button"
              >
                Add
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default LaserCanvas; 