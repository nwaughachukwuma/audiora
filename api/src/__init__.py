import asyncio
import os
import sys
from pathlib import Path

import uvloop
from dotenv import load_dotenv

## Begin: Add the project root to sys.path
project_root = Path(__file__).parent.parent.resolve()
sys.path.append(str(project_root))

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
print("running uvloop as event loop policy for asyncio")

load_dotenv()


def init_shared_packages(paths: list[str]):
    # Add the shared module directory to the Python path
    for path in paths:
        pkg_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", path))
        sys.path.append(pkg_path)


init_shared_packages(["services", "utils_pkg"])
print(f"Project root: {project_root}")
