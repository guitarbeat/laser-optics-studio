#!/bin/bash
# Compile script for optical diagrams

# Verify that a file is provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <file.tex> [--open]"
    echo "Example: $0 src/schematics/my_diagram.tex --open"
    exit 1
fi

# Get the file path
FILE=$1
OPEN_PDF=false

# Check for --open flag
if [ "$2" == "--open" ]; then
    OPEN_PDF=true
fi

# Verify file exists
if [ ! -f "$FILE" ]; then
    echo "Error: File $FILE not found!"
    exit 1
fi

# Determine base file name and directory
BASE=$(basename "$FILE" .tex)
DIR=$(dirname "$FILE")

# Determine target directory based on source directory
if [[ $DIR == *"schematics"* ]]; then
    TARGET=build/schematics
elif [[ $DIR == *"tests"* ]]; then
    TARGET=build/tests
elif [[ $DIR == *"docs"* ]]; then
    TARGET=build/docs
elif [[ $DIR == *"cheatsheets"* ]]; then
    TARGET=build/cheatsheets
else
    echo "Unknown source directory: $DIR"
    echo "Creating output in build/output"
    TARGET=build/output
    mkdir -p $TARGET
fi

echo "Compiling $FILE to $TARGET/$BASE.pdf"
mkdir -p $TARGET

# Run XeLaTeX (twice to resolve references)
xelatex -output-directory=$TARGET $FILE
if [ $? -ne 0 ]; then
    echo "Error: XeLaTeX compilation failed!"
    exit 1
fi

xelatex -output-directory=$TARGET $FILE
if [ $? -ne 0 ]; then
    echo "Warning: Second XeLaTeX pass failed, but PDF may still be usable."
fi

# Clean up auxiliary files
echo "Cleaning up auxiliary files..."
rm -f $TARGET/$BASE.aux $TARGET/$BASE.log

# Check if PDF was created
if [ -f "$TARGET/$BASE.pdf" ]; then
    echo "Success! PDF created at $TARGET/$BASE.pdf"
    
    # Open the PDF if requested
    if [ "$OPEN_PDF" = true ]; then
        if command -v open &> /dev/null; then
            echo "Opening PDF..."
            open $TARGET/$BASE.pdf
        elif command -v xdg-open &> /dev/null; then
            echo "Opening PDF..."
            xdg-open $TARGET/$BASE.pdf
        else
            echo "Could not open PDF automatically. Please open $TARGET/$BASE.pdf manually."
        fi
    fi
else
    echo "Error: PDF creation failed!"
    exit 1
fi

exit 0 