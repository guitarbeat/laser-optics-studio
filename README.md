# Laser Optics Studio

Monorepo combining two complementary projects for laser/optics work:

- apps/laser-diagram-tool — Python/Tkinter GUI for creating optical diagrams and exporting LaTeX (pst-optexp)
- apps/optics-canvas — React + Express app for an interactive laser optics canvas with a component library and CSV-backed data grid

The full Git history of the original repositories is preserved using git subtree.

## Quick Start

Prerequisites:
- Python 3.10+
- Node.js 18+
- npm 8+

Common tasks:

```bash
# from repo root
make setup          # install Python deps for laser-diagram-tool and npm deps for optics-canvas
make run-lasers     # run the Python laser diagram tool
make run-optics     # run the React + Express optics canvas (client on :3000, API on :3001)
```

If you prefer manual steps:

```bash
# Laser Diagram Tool (Python)
cd apps/laser-diagram-tool
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 src/main.py

# Optics Canvas (React + Express)
cd apps/optics-canvas
npm install
npm run dev
```

## Repository Structure

```
.
├─ apps/
│  ├─ laser-diagram-tool/   # Python GUI app (Tkinter) with LaTeX export
│  └─ optics-canvas/        # React client + Express server
├─ README.md                 # This file
├─ .gitignore                # Node, Python, OS ignores
└─ Makefile                  # Convenience commands
```

## Notes

- For the optics canvas assets and persistence details, see `apps/optics-canvas/README.md`. The app serves a canvas powered by React Flow and persists CSV via an API server. Reference: `apps/optics-canvas/README.md` and project documentation inspired by `optics` repository notes [`guitarbeat/optics`](https://github.com/guitarbeat/optics).
- For the laser diagram tool capabilities (components, LaTeX generation), see `apps/laser-diagram-tool/README.md` and docs under `apps/laser-diagram-tool/docs`.

## Contributing

Use conventional commits where possible. Run each app locally before submitting changes. Python/JS tooling is isolated per app.

## License

Each app retains its original license/attribution files within its directory.
