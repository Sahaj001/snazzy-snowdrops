async function loadProject(pyodide) {
    const response = await fetch('../dist/src.zip'); // served from dist
    let buffer = await response.arrayBuffer();

    await pyodide.unpackArchive(buffer, 'zip'); // by default, unpacks to the current dir

    console.log('Project loaded...');
}

async function loadStatusBar() {
    const response = await fetch('src/ui/components/statusbar.html');
    const html = await response.text();
    document.getElementById('hud-container').innerHTML = html;
}

async function loadMenu() {
    const response = await fetch('src/ui/components/menu.html');
    const html = await response.text();
    document.getElementById('menu-container').innerHTML = html;
}

async function main() {
    await loadMenu();
    console.log('Loading Pyodide...');
    const pyodide = await loadPyodide();
    pyodide.setDebug(true);

    console.log('Loading python project...');
    await loadProject(pyodide);

    console.log('Loading Python packages...');
    await pyodide.runPythonAsync(`
        import sys
        sys.path.append('/src')
        import main
        await main.start()
    `);

    await loadStatusBar();


}

main();
