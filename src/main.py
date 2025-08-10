import http.server
import os
import shutil
import socketserver
from pathlib import Path


def main() -> None:
    # Detect project root (two levels up if main.py is in src/)
    root_dir = Path(__file__).resolve().parent
    if (root_dir / "src").exists() and (root_dir / "web").exists():
        project_root = root_dir
    elif (root_dir.parent / "src").exists() and (root_dir.parent / "web").exists():
        project_root = root_dir.parent
    else:
        msg = "Could not locate src/ and web/ directories"
        raise FileNotFoundError(msg)

    src_dir = project_root / "src"
    web_dir = project_root / "web"

    if not src_dir.exists():
        msg = f"src directory not found: {src_dir}"
        raise FileNotFoundError(msg)
    if not web_dir.exists():
        msg = f"web directory not found: {web_dir}"
        raise FileNotFoundError(msg)

    # Create src.zip for Pyodide to load
    zip_path = web_dir / "src.zip"
    shutil.make_archive(zip_path.with_suffix(""), "zip", src_dir)

    # Serve from the web directory
    os.chdir(web_dir)
    PORT = 8000
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
