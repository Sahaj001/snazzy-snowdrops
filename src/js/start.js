async function main() {
    let pyodide = await loadPyodide();

    // Make canvas available to Python
    pyodide.globals.set("canvas", document.getElementById("canvas"));
    pyodide.globals.set("window", window);

    // Load and execute the Python file
    const response = await fetch('./main.py');
    const pythonCode = await response.text();
    pyodide.runPython(pythonCode);

    // Handle window resize
    window.addEventListener('resize', () => {
        pyodide.runPython(`
            import main
            main.resize_canvas()
        `);
    });
}

// Start the application
main();
