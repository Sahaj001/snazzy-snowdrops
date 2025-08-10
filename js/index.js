async function loadProject(pyodide) {

    const response = await fetch('../dist/src.zip'); // served from dist
    let buffer = await response.arrayBuffer();

    await pyodide.unpackArchive(buffer, "zip"); // by default, unpacks to the current dir

    console.log("Project loaded...");
}

async function main() {
    console.log("Loading Pyodide...");
    const pyodide = await loadPyodide();
    pyodide.setDebug(true)

    console.log("Loading python project...")
    await loadProject(pyodide);

    console.log("Loading Python packages...");
    await pyodide.runPythonAsync(`
        import sys
        import main
    `);


    // Make the canvas available to Python
    const canvas = document.getElementById("gameCanvas");
    pyodide.globals.set("canvas", canvas);

    await pyodide.runPythonAsync("import sys; sys.path.append('/src'); import main");
}

main();
