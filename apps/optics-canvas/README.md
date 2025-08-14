# Laser Components Canvas

An interactive React application for designing laser optics experiments. It combines a searchable component library and a drag-and-drop canvas editor with a data grid for managing component metadata. A lightweight Node/Express server persists the data grid to CSV.

- Live canvas powered by React Flow
- Data grid powered by AG Grid
- Assets copied from `ComponentLibrary_files` to `public/ComponentLibrary_files` on start

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Scripts](#scripts)
- [Project Structure](#project-structure)
- [Data Model](#data-model)
- [API](#api)
- [Using the App](#using-the-app)
  - [Data Grid](#data-grid)
  - [Canvas Editor](#canvas-editor)
- [Assets and Component Library](#assets-and-component-library)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License & Attribution](#license--attribution)

## Features

- **Component Library**: Browse and search a library of laser optics components
- **Drag-and-Drop Canvas**: Place, move, and connect components visually
- **Resizable Components**: Scale components within constraints
- **Text Labels**: Annotate designs with editable labels
- **Connection Lines**: Connect components to indicate beam paths
- **Layouts**: Save and load designs locally in the canvas editor
- **Data Grid**: View and edit component metadata in a tabular view
- **CSV Persistence**: Save grid changes to `public/data.csv` via the server, with localStorage fallback

## Requirements

- Node.js 18+ recommended
- npm 8+

## Quick Start

1. Install dependencies
   ```bash
   npm install
   ```
2. Start the client and API server together (recommended during development)
   ```bash
   npm run dev
   ```
   - Client: `http://localhost:3000`
   - API server: `http://localhost:3001`

Notes
- A prestart hook copies `ComponentLibrary_files` into `public/ComponentLibrary_files` (see [Assets](#assets-and-component-library)).
- The CRA dev server proxies API requests to `http://localhost:3001`.

## Scripts

- `npm start`: Start the React app only (runs prestart copy step)
- `npm run server`: Start the Express API server on port 3001
- `npm run dev`: Start client and server concurrently
- `npm run build`: Build the React app for production
- `npm test`: Run tests (if any are added)
- `npm run copy-components`: Manually copy assets to `public/ComponentLibrary_files`

## Project Structure

```
.
├─ public/
│  ├─ index.html
│  ├─ data.csv
│  └─ ComponentLibrary_files/      # Copied assets for the canvas component library
├─ src/
│  ├─ components/
│  │  ├─ LaserCanvas.js            # Canvas editor and React Flow integration
│  │  └─ LaserCanvas.css
│  ├─ App.js                       # Tabbed UI: Data Grid and Canvas Editor
│  ├─ index.js
│  └─ index.css
├─ server.js                        # Express server; saves CSV and serves production build
├─ copyComponents.js                # Copies ComponentLibrary_files to public
├─ data.csv                         # Source CSV (initially copied/used by public/data.csv)
├─ ComponentLibrary_files/          # Source assets to be copied to public/
├─ package.json
└─ README.md
```

## Data Model

The data grid loads from `public/data.csv` and expects headers like:

- `position`: row order (stringified integer)
- `Element`: component element name
- `System`: system/category
- `Model`: model identifier

Notes
- The grid includes a drag handle column (not persisted).
- When rows are edited or reordered, the app attempts to save the entire grid to CSV via the API.

## API

Base URL in development: `http://localhost:3001`

- `POST /api/save-data`
  - Content-Type: `text/plain`
  - Body: CSV string (the full grid)
  - Effect: Overwrites `public/data.csv`
  - Response: `{ success: boolean, message: string }`

If the request fails, the app falls back to saving the CSV in `localStorage` under the key `laser-components-data`.

## Using the App

### Data Grid
- Load: The grid fetches `public/data.csv` at startup
- Edit: Cells are directly editable; changes are auto-saved with debounce
- Reorder: Drag rows to update `position`; saves immediately
- Export: Use “Download CSV” to download the current grid

### Canvas Editor
- **Component Library**
  - Browse, search, and filter by category:
    - Beam Control (prefix `b-`)
    - Complex Components (prefix `c-`)
    - Electronic Components (prefix `e-`)
- **Add Components**
  - Click items in the library or from the database list to add to the canvas
  - Add text labels via the “Add Label” action
- **Manipulate**
  - Move: drag components to reposition
  - Resize: drag the bottom-right handle
  - Delete: click the × icon or press Delete when selected
  - Edit labels: double-click a text label
- **Connect**
  - Drag from a handle (left/right/top/bottom) to another component to form connections
- **Layouts**
  - Save, load, delete, and clear the current canvas layout

## Assets and Component Library

The canvas uses vector graphics from Alexander Franzen’s ComponentLibrary (2006). On start:
- `copyComponents.js` copies `ComponentLibrary_files/` to `public/ComponentLibrary_files/`.
- Ensure the source directory exists and contains the expected assets.

Reference: `http://www.gwoptics.org/component_library/`

## Deployment

Production build served by the Express server:

```bash
npm run build
npm run server
# Open http://localhost:3001
```

- The server serves static files from `build/` and handles `POST /api/save-data`.
- Ensure the process has write permissions to `public/data.csv` if persistence is required in production.

## Troubleshooting

- Ports in use (3000 or 3001): stop conflicting processes or change ports via env vars
- Missing or broken component images: run `npm run copy-components` or ensure the prestart hook ran
- CSV not saving: confirm API server is running, check console/network tab, and filesystem write permissions

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for development setup and contribution guidelines.

## License & Attribution

- ComponentLibrary by Alexander Franzen is licensed under Creative Commons Attribution-NonCommercial 3.0 Unported.
- This application is intended for educational and research purposes only.
- Third-party attributions are listed in [THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md). 