# Contributing

Thanks for your interest in contributing! This guide explains how to set up your environment, run the app, and propose changes.

## Development Setup

1. Prerequisites
   - Node.js 18+
   - npm 8+

2. Install dependencies
   ```bash
   npm install
   ```

3. Start development servers
   ```bash
   npm run dev
   ```
   - Client: http://localhost:3000
   - API: http://localhost:3001

Notes
- A prestart step copies `ComponentLibrary_files/` to `public/ComponentLibrary_files/`.
- The client proxies API requests to the server.

## Project Conventions

- Code style: match existing formatting and patterns
- Naming: prefer descriptive, full-word names for variables and functions
- Types: when adding new modules, include JSDoc for complex functions
- Control flow: prefer early returns and guard clauses
- Avoid deep nesting; extract helpers for clarity

## Testing

- Add tests for new logic where practical
- Keep UI tests deterministic and scoped

## Making Changes

1. Create a feature branch
2. Make focused commits with clear messages
3. Ensure the app builds and runs without errors
   ```bash
   npm run build
   npm run server
   ```
4. Open a pull request
   - Describe the change, rationale, and any trade-offs
   - Include screenshots or GIFs for UI changes

## Areas to Improve

- Add automated tests for core grid and canvas behaviors
- Factor large components (e.g., `src/components/LaserCanvas.js`) into smaller units
- Improve accessibility and keyboard interactions in the canvas
- Add CI to run build and basic checks

## Security & Privacy

- Do not commit secrets or credentials
- Sanitize any user-provided input rendered in the UI

## License

By contributing, you agree that your contributions will be licensed under the repository’s license and that third-party asset attributions remain intact.