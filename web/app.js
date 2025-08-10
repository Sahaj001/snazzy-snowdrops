import { loadPyodide } from "https://cdn.jsdelivr.net/pyodide/v0.28.1/full/pyodide.mjs";

async function main() {
    console.log("Loading Pyodide...");
    const pyodide = await loadPyodide({
        indexURL: "https://cdn.jsdelivr.net/pyodide/v0.28.1/full/"
    });
    console.log("Pyodide loaded");

    // Give Python access to the JS canvas API
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    pyodide.globals.set("js_canvas", canvas);
    pyodide.globals.set("js_ctx", ctx);

    // Load src.zip
    const response = await fetch("src.zip");
    const buffer = await response.arrayBuffer();
    pyodide.unpackArchive(buffer, "zip");

    await pyodide.runPythonAsync(`
        import sys
        if "/src" not in sys.path:
            sys.path.append("/src")
        import game
        game.start()
    `);
}

main();
