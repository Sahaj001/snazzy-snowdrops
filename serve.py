from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryFile
from typing import TYPE_CHECKING
from zipfile import ZipFile

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse, Response
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

if TYPE_CHECKING:
    from starlette.requests import Request


async def root(_request: Request) -> Response:
    return FileResponse("index.html")


async def srczip(_request: Request) -> Response:
    src = Path("src")
    with TemporaryFile("r+b") as tempfile, ZipFile(tempfile, "w") as zipfile:
        for path in src.glob("**/*.py"):
            zipfile.write(path, path.relative_to(src))
        zipfile.close()
        tempfile.seek(0)
        content = tempfile.read()
        return Response(content, media_type="application/json")


app = Starlette(
    routes=[
        Route("/", root),
        Route("/src.zip", srczip),
        Mount("/static", app=StaticFiles(directory="static"), name="static"),
    ],
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ],
)
