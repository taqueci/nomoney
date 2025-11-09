const fs = require('fs/promises');
const path = require('path');
const process = require('process');

/**
 * Processes an array of files/directories and copies them.
 * @param {Array<Object>} files - An array of objects containing the
 * source path (from) and destination path (to).
 * @returns {boolean} Returns true if all copies were successful, otherwise
 * false.
 */
async function copyFiles(files) {
  let allSucceeded = true;

  for (const file of files) {
    const { from, to } = file;

    try {
      const stats = await fs.stat(from);

      if (stats.isDirectory()) {
        console.log(`Copying directory '${from}' -> '${to}'`);
        await fs.cp(from, to, { recursive: true });
      } else {
        const destDir = path.dirname(to);
        await fs.mkdir(destDir, { recursive: true });

        console.log(`Copying file '${from}' -> '${to}'`);
        await fs.copyFile(from, to);
      }
    } catch (error) {
      console.error(`Failed to copy '${from}': ${error.message}`);
      allSucceeded = false;
    }
  }

  return allSucceeded;
}

/**
 * Main function to handle argument parsing and execution.
 */
async function main() {
  const jsonFilePath = process.argv[2];

  if (!jsonFilePath) {
    console.error('Usage: node copyFiles.js COPY_LIST.json');
    process.exit(1);
  }

  let filesToCopy = [];

  try {
    const data = await fs.readFile(jsonFilePath, { encoding: 'utf8' });
    filesToCopy = JSON.parse(data);

    if (!Array.isArray(filesToCopy)) {
      throw new Error("JSON content must be an array of file objects.");
    }

    console.log(`Successfully loaded copy list from ${jsonFilePath}`);
  } catch (error) {
    console.error(`Failed to read/parse '${jsonFilePath}': ${error.message}`);
    process.exit(1);
  }

  copyFiles(filesToCopy)
    .then(allSucceeded => {
      if (allSucceeded) {
        console.log(`${filesToCopy.length} files have been copied.`);
        process.exit(0);
      } else {
        process.exit(1);
      }
    })
    .catch(error => {
      process.exit(1);
    });
}

main();
