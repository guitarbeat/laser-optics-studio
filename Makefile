# Makefile for PSTricks/PST-optexp automation - Improved Structure
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
#   make debug          # Show variables for debugging
#   make test           # Test build system with simple cheatsheet
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

# Direct PDF generation using pdflatex with proper options for PSTricks
build/schematics/%.pdf: src/schematics/%.tex
	@mkdir -p $(dir $@)
	xelatex -output-directory=$(dir $@) $<
	@if [ -f $(dir $@)$*.aux ]; then \
		xelatex -output-directory=$(dir $@) $<; \
	fi

build/tests/%.pdf: src/tests/%.tex
	@mkdir -p $(dir $@)
	xelatex -output-directory=$(dir $@) $<
	@if [ -f $(dir $@)$*.aux ]; then \
		xelatex -output-directory=$(dir $@) $<; \
	fi

build/docs/%.pdf: src/docs/%.tex
	@mkdir -p $(dir $@)
	xelatex -output-directory=$(dir $@) $<
	@if [ -f $(dir $@)$*.aux ]; then \
		xelatex -output-directory=$(dir $@) $<; \
	fi

build/cheatsheets/%.pdf: src/cheatsheets/%.tex
	@mkdir -p $(dir $@)
	xelatex -output-directory=$(dir $@) $<
	@if [ -f $(dir $@)$*.aux ]; then \
		xelatex -output-directory=$(dir $@) $<; \
	fi

# Debug target to print variable values
debug:
	@echo "SCHEMATIC_TEX: $(SCHEMATIC_TEX)"
	@echo "SCHEMATIC_PDF: $(SCHEMATIC_PDF)"
	@echo "TEST_TEX: $(TEST_TEX)" 
	@echo "TEST_PDF: $(TEST_PDF)"
	@echo "CHEATSHEET_TEX: $(CHEATSHEET_TEX)"
	@echo "CHEATSHEET_PDF: $(CHEATSHEET_PDF)"
	@echo "DOC_TEX: $(DOC_TEX)"
	@echo "DOC_PDF: $(DOC_PDF)"

# Test target to verify build system
test:
	@echo "Testing build system..."
	$(MAKE) build/cheatsheets/simple_cheatsheet.pdf
	@echo "Test complete. Check build/cheatsheets/simple_cheatsheet.pdf"

clean:
	rm -rf build 