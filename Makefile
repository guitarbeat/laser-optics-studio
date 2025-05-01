# Makefile for PSTricks/PST-optexp automation - Project-based structure
#
# Directory Structure:
#   projects/          # Main projects directory
#     project1/        # First project
#       schematics/    # Schematic diagrams for project1
#       tests/         # Test files for project1
#       docs/          # Documentation for project1
#     project2/        # Second project
#       schematics/    # Schematic diagrams for project2
#       tests/         # Test files for project2
#       docs/          # Documentation for project2
#   common/            # Common resources shared across projects
#     cheatsheets/     # Reference cheatsheets
#     templates/       # Template files
#   build/             # Output directory
#     project1/        # Built PDFs for project1
#     project2/        # Built PDFs for project2
#     common/          # Built PDFs for common resources
#
# Usage:
#   make                    # Build default targets (simple example)
#   make all                # Build all PDFs from all projects
#   make project-[name]     # Build all PDFs for a specific project
#   make cheatsheets        # Build all PDFs in common/cheatsheets/
#   make clean              # Remove all generated files in build/
#
# Rules:
#   all:                Build all projects
#   project-[name]:     Build specific project (e.g., make project-basic_laser)
#   cheatsheets:        Build all PDFs from common/cheatsheets/
#   build/project1/%.pdf: Build PDF from project1/%.tex
#   clean:              Remove all generated files
#
# To add new projects, create new directories under projects/

# Default target is a simple example
all: default-example

# Create output directories
build-dirs:
	mkdir -p build/common/cheatsheets

# Default projects (add your projects to this list)
PROJECTS := basic_laser advanced_imaging

# Define a pattern rule to create build directories for each project
define make-project-build-dir
build/$(1):
	mkdir -p build/$(1)/schematics build/$(1)/tests build/$(1)/docs
endef

# Apply the rule to each project
$(foreach proj,$(PROJECTS),$(eval $(call make-project-build-dir,$(proj))))

# Build all projects
all-projects: $(foreach proj,$(PROJECTS),project-$(proj))

# Pattern rule for building a specific project
project-%: build/%
	@echo "Building project $*..."
	$(MAKE) $(foreach dir,schematics tests docs,$(patsubst projects/$*/$(dir)/%.tex,build/$*/$(dir)/%.pdf,$(wildcard projects/$*/$(dir)/*.tex)))

# Cheatsheets
CHEATSHEET_TEX := $(wildcard common/cheatsheets/*.tex)
CHEATSHEET_PDF := $(patsubst common/cheatsheets/%.tex,build/common/cheatsheets/%.pdf,$(CHEATSHEET_TEX))

cheatsheets: build-dirs $(CHEATSHEET_PDF)

# Default example target (modify as needed)
default-example: build-dirs
	@if [ -f projects/basic_laser/schematics/simple_schematic.tex ]; then \
		$(MAKE) build/basic_laser/schematics/simple_schematic.pdf; \
	else \
		echo "Simple example not found. Run 'make migrate' to set up project structure."; \
	fi

# Pattern rules for tex files in project directories
build/%/schematics/%.dvi: projects/%/schematics/%.tex
	@mkdir -p $(dir $@)
	latex -output-directory=$(dir $@) $<

build/%/tests/%.dvi: projects/%/tests/%.tex
	@mkdir -p $(dir $@)
	latex -output-directory=$(dir $@) $<

build/%/docs/%.dvi: projects/%/docs/%.tex
	@mkdir -p $(dir $@)
	latex -output-directory=$(dir $@) $<

# Pattern rules for common resources
build/common/cheatsheets/%.dvi: common/cheatsheets/%.tex
	@mkdir -p $(dir $@)
	latex -output-directory=$(dir $@) $<

# General rules for PS and PDF conversion
build/%.ps: build/%.dvi
	dvips $< -o $@

build/%.pdf: build/%.ps
	ps2pdf $< $@
	@rm -f $< $*.dvi

# Migration target - helps migrate from old structure to new project structure
migrate: build-dirs
	@echo "Creating project structure..."
	@mkdir -p projects/basic_laser/schematics projects/basic_laser/tests projects/basic_laser/docs
	@mkdir -p projects/advanced_imaging/schematics projects/advanced_imaging/tests projects/advanced_imaging/docs
	@mkdir -p common/cheatsheets common/templates
	@if [ -d tex/schematics ]; then \
		cp tex/schematics/simple_schematic.tex projects/basic_laser/schematics/ 2>/dev/null || true; \
		cp tex/schematics/imaging_system_schematic.tex projects/advanced_imaging/schematics/ 2>/dev/null || true; \
		echo "Migrated schematic files"; \
	fi
	@if [ -d tex/tests ]; then \
		cp tex/tests/simple_test.tex projects/basic_laser/tests/ 2>/dev/null || true; \
		echo "Migrated test files"; \
	fi
	@if [ -d tex/cheatsheets ]; then \
		cp tex/cheatsheets/*.tex common/cheatsheets/ 2>/dev/null || true; \
		echo "Migrated cheatsheet files"; \
	fi
	@echo "Migration complete. New structure is ready."

clean:
	rm -rf build 