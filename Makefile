SHELL := /bin/bash

# * Setup both apps
setup:
	# Python app deps
	cd apps/laser-diagram-tool && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
	# JS app deps
	cd apps/optics-canvas && npm install

# * Run Python laser diagram tool
run-lasers:
	cd apps/laser-diagram-tool && source .venv/bin/activate && python3 src/main.py

# * Run optics canvas (client+server)
run-optics:
	cd apps/optics-canvas && npm run dev

# * Build optics client
build-optics:
	cd apps/optics-canvas && npm run build

.PHONY: setup run-lasers run-optics build-optics

