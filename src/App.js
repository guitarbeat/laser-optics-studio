import React, { useState, useEffect, useCallback, useRef } from 'react';
import { AgGridReact } from 'ag-grid-react';
import Papa from 'papaparse';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import LaserCanvas from './components/LaserCanvas';

export default function App() {
  const [rowData, setRowData] = useState([]);
  const [saveStatus, setSaveStatus] = useState('');
  const [activeTab, setActiveTab] = useState('grid'); // 'grid' or 'canvas'
  const gridRef = useRef(null);
  const saveTimeoutRef = useRef(null);
  
  // load the CSV once on mount
  useEffect(() => {
    fetch('/data.csv')
      .then(res => res.text())
      .then(csv => {
        Papa.parse(csv, {
          header: true,
          skipEmptyLines: true,
          complete: results => {
            // Add position index if not present
            const dataWithPosition = results.data.map((row, index) => ({
              ...row,
              position: row.position || (index + 1).toString()
            }));
            setRowData(dataWithPosition);
          }
        });
      })
      .catch(err => {
        console.error('Error loading data:', err);
        setSaveStatus('Error loading data');
      });
  }, []);

  const [columnDefs] = useState([
    { field: 'position', headerName: 'Position', width: 100, editable: true },
    { field: 'drag', rowDrag: true, headerName: '', width: 40 },
    { field: 'Element', sortable: true, filter: true, editable: true },
    { field: 'System', sortable: true, filter: true, editable: true },
    { field: 'Model', sortable: true, filter: true, editable: true },
  ]);

  // Debounce function to prevent too many saves
  const debounce = (func, delay) => {
    return (...args) => {
      if (saveTimeoutRef.current) {
        clearTimeout(saveTimeoutRef.current);
      }
      saveTimeoutRef.current = setTimeout(() => {
        func(...args);
      }, delay);
    };
  };

  // Save data with debounce
  const debouncedSave = useCallback(
    debounce((data) => {
      saveDataToServer(data);
    }, 1000),
    []
  );

  // Handle cell value changes
  const onCellValueChanged = useCallback((params) => {
    // Update the data
    const updatedData = [];
    gridRef.current.api.forEachNode((node) => {
      updatedData.push(node.data);
    });
    setRowData(updatedData);
    
    // Auto-save with debounce
    setSaveStatus('Editing...');
    debouncedSave(updatedData);
  }, [debouncedSave]);

  // Save data when rows are reordered
  const onRowDragEnd = useCallback(() => {
    if (gridRef.current) {
      const updatedData = [];
      gridRef.current.api.forEachNode((node, index) => {
        updatedData.push({
          ...node.data,
          position: (index + 1).toString()
        });
      });
      setRowData(updatedData);
      setSaveStatus('Saving...');
      saveDataToServer(updatedData);
    }
  }, []);

  // Function to save data to server
  const saveDataToServer = (data) => {
    const csv = Papa.unparse(data);
    setSaveStatus('Saving...');
    
    // In a real app with backend, use this:
    fetch('/api/save-data', {
      method: 'POST',
      headers: {
        'Content-Type': 'text/plain',
      },
      body: csv
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setSaveStatus('Changes saved');
        setTimeout(() => setSaveStatus(''), 3000);
      })
      .catch(error => {
        console.error('Error saving data:', error);
        setSaveStatus('Error saving');
        
        // Fallback to localStorage if server save fails
        localStorage.setItem('laser-components-data', csv);
      });
  };

  // Button to manually save data as CSV
  const handleDownloadCSV = () => {
    if (gridRef.current) {
      const dataToSave = [];
      gridRef.current.api.forEachNode((node) => {
        dataToSave.push(node.data);
      });
      
      const csv = Papa.unparse(dataToSave);
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      const url = URL.createObjectURL(blob);
      link.setAttribute('href', url);
      link.setAttribute('download', 'laser_components.csv');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  // Tab styles
  const tabStyle = {
    padding: '10px 20px',
    backgroundColor: '#333',
    color: '#fff',
    border: 'none',
    borderRadius: '4px 4px 0 0',
    cursor: 'pointer',
    marginRight: '5px',
    fontSize: '16px',
    fontWeight: 'bold',
  };

  const activeTabStyle = {
    ...tabStyle,
    backgroundColor: '#4CAF50',
  };

  return (
    <div style={{ padding: '20px', backgroundColor: '#1e1e1e', minHeight: '100vh' }}>
      <h1 style={{ color: '#ffffff', textAlign: 'center' }}>Laser Components</h1>
      
      {/* Tab Navigation */}
      <div style={{ display: 'flex', marginBottom: '20px' }}>
        <button 
          style={activeTab === 'grid' ? activeTabStyle : tabStyle}
          onClick={() => setActiveTab('grid')}
        >
          Data Grid
        </button>
        <button 
          style={activeTab === 'canvas' ? activeTabStyle : tabStyle}
          onClick={() => setActiveTab('canvas')}
        >
          Canvas Editor
        </button>
      </div>

      {/* Tab Content */}
      {activeTab === 'grid' && (
        <>
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            marginBottom: '10px', 
            padding: '0 10px'
          }}>
            <div style={{ 
              color: saveStatus === 'Saving...' || saveStatus === 'Editing...' ? '#FFA500' : 
                    saveStatus === 'Error saving' ? '#FF0000' : '#4CAF50',
              transition: 'opacity 0.3s',
              opacity: saveStatus ? 1 : 0,
              fontWeight: 'bold'
            }}>
              {saveStatus}
            </div>
            <div>
              <button 
                onClick={handleDownloadCSV}
                style={{
                  padding: '8px 16px',
                  backgroundColor: '#4CAF50',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  marginLeft: '10px'
                }}
              >
                Download CSV
              </button>
            </div>
          </div>
          <div 
            className="ag-theme-alpine-dark" 
            style={{ 
              width: '800px', 
              height: '600px', 
              margin: 'auto',
              '--ag-background-color': '#222',
              '--ag-odd-row-background-color': '#333',
              '--ag-header-background-color': '#111',
              '--ag-foreground-color': '#fff',
              '--ag-border-color': '#444'
            }}
          >
            <AgGridReact
              ref={gridRef}
              columnDefs={columnDefs}
              rowData={rowData}
              rowDragManaged={true}
              animateRows={true}
              onRowDragEnd={onRowDragEnd}
              onCellValueChanged={onCellValueChanged}
              rowClassRules={{
                'ag-row-dark': 'true'
              }}
              stopEditingWhenCellsLoseFocus={true}
              singleClickEdit={true}
              editType="fullRow"
            />
          </div>
        </>
      )}

      {activeTab === 'canvas' && (
        <LaserCanvas />
      )}
    </div>
  );
} 