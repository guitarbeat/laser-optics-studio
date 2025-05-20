const fs = require('fs-extra');
const path = require('path');

// Source and destination paths
const sourceDir = path.join(__dirname, 'ComponentLibrary_files');
const destDir = path.join(__dirname, 'public', 'ComponentLibrary_files');

// Copy function
async function copyComponentLibrary() {
  try {
    console.log(`Copying from ${sourceDir} to ${destDir}...`);
    
    // Ensure the destination directory exists
    await fs.ensureDir(path.dirname(destDir));
    
    // Copy the directory recursively
    await fs.copy(sourceDir, destDir, {
      overwrite: true,
      errorOnExist: false
    });
    
    console.log('Component library files copied successfully to public directory!');
  } catch (err) {
    console.error('Error copying component library files:', err);
  }
}

// Execute the copy
copyComponentLibrary(); 