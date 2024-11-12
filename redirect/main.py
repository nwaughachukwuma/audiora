import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

load_dotenv()

API_URL = os.environ["API_URL"]


@app.get("/{full_path:path}")
def read_root_get(full_path: str):
    return RedirectResponse(url=API_URL)


@app.post("/{full_path:path}")
def read_root_post(full_path: str):
    return RedirectResponse(url=API_URL)


@app.put("/{full_path:path}")
def read_root_put(full_path: str):
    return RedirectResponse(url=API_URL)


@app.delete("/{full_path:path}")
def read_root_delete(full_path: str):
    return RedirectResponse(url=API_URL)


@app.patch("/{full_path:path}")
def read_root_patch(full_path: str):
    return RedirectResponse(url=API_URL)


@app.options("/{full_path:path}")
def read_root_options(full_path: str):
    return RedirectResponse(url=API_URL)


@app.head("/{full_path:path}")
def read_root_head(full_path: str):
    return RedirectResponse(url=API_URL)
