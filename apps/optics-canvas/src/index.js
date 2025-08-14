import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import './index.css';               // we'll import the ag-Grid themes here

createRoot(document.getElementById('root')).render(<App />); 