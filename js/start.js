async function main() {
    console.log("Loading Pyodide...");
    let pyodide = await loadPyodide();
    console.log("Pyodide loaded");
    let code = await (await fetch("src/main.py")).text();
    await pyodide.runPythonAsync(code);
    console.log("Python code running");
}
main();
