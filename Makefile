# Makefile for PSTricks/PST-optexp automation - Simplified Structure
#
# Directory Structure:
#   src/                # Main source directory
#     schematics/       # Schematic diagrams
#     tests/            # Test files
#     docs/             # Documentation
#     templates/        # Template files
#     cheatsheets/      # Reference cheatsheets
#   build/              # Output directory
#     schematics/       # Built schematic PDFs
#     tests/            # Built test PDFs
#     docs/             # Built documentation PDFs
#     cheatsheets/      # Built cheatsheet PDFs
#
# Usage:
#   make                # Build default targets (imaging_system_schematic.pdf)
#   make all            # Build all PDFs
#   make schematics     # Build all PDFs in src/schematics/
#   make tests          # Build all PDFs in src/tests/
#   make docs           # Build all PDFs in src/docs/
#   make cheatsheets    # Build all PDFs in src/cheatsheets/
#   make clean          # Remove all generated files in build/
#
# Rules:
#   all:                Build all PDFs
#   schematics:         Build all PDFs from src/schematics/
#   tests:              Build all PDFs from src/tests/
#   docs:               Build all PDFs from src/docs/
#   cheatsheets:        Build all PDFs from src/cheatsheets/
#   build/%.pdf:        Build PDF from src/%.tex
#   clean:              Remove all generated files
#
# To add new files, place them in the appropriate src/ subdirectory.

# Default target builds the imaging system schematic
all: default-target

# Create output directories
build-dirs:
	mkdir -p build/schematics build/tests build/docs build/cheatsheets

# Find all tex files in subdirectories
SCHEMATIC_TEX := $(wildcard src/schematics/*.tex)
TEST_TEX := $(wildcard src/tests/*.tex)
DOC_TEX := $(wildcard src/docs/*.tex)
CHEATSHEET_TEX := $(wildcard src/cheatsheets/*.tex)
ALL_TEX := $(SCHEMATIC_TEX) $(TEST_TEX) $(DOC_TEX) $(CHEATSHEET_TEX)

# Generate corresponding PDF targets
SCHEMATIC_PDF := $(patsubst src/schematics/%.tex,build/schematics/%.pdf,$(SCHEMATIC_TEX))
TEST_PDF := $(patsubst src/tests/%.tex,build/tests/%.pdf,$(TEST_TEX))
DOC_PDF := $(patsubst src/docs/%.tex,build/docs/%.pdf,$(DOC_TEX))
CHEATSHEET_PDF := $(patsubst src/cheatsheets/%.tex,build/cheatsheets/%.pdf,$(CHEATSHEET_TEX))
ALL_PDF := $(SCHEMATIC_PDF) $(TEST_PDF) $(DOC_PDF) $(CHEATSHEET_PDF)

# Default target
default-target: build-dirs
	@if [ -f src/schematics/imaging_system_schematic.tex ]; then \
		$(MAKE) build/schematics/imaging_system_schematic.pdf; \
	else \
		echo "Imaging system schematic not found."; \
	fi

# Build targets for each category
schematics: build-dirs $(SCHEMATIC_PDF)
tests: build-dirs $(TEST_PDF)
docs: build-dirs $(DOC_PDF)
cheatsheets: build-dirs $(CHEATSHEET_PDF)

# Build all PDFs target
all-pdfs: schematics tests docs cheatsheets

# Pattern rules for tex files in src subdirectories
build/schematics/%.dvi: src/schematics/%.tex
	@mkdir -p $(dir $@)
	latex -output-directory=$(dir $@) $<

build/tests/%.dvi: src/tests/%.tex
	@mkdir -p $(dir $@)
	latex -output-directory=$(dir $@) $<

build/docs/%.dvi: src/docs/%.tex
	@mkdir -p $(dir $@)
	latex -output-directory=$(dir $@) $<

build/cheatsheets/%.dvi: src/cheatsheets/%.tex
	@mkdir -p $(dir $@)
	latex -output-directory=$(dir $@) $<

# General rules for PS and PDF conversion
build/%.ps: build/%.dvi
	dvips $< -o $@

build/%.pdf: build/%.ps
	ps2pdf $< $@
	@rm -f $< $*.dvi

clean:
	rm -rf build 