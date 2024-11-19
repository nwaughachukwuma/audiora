import asyncio
import sys
from pathlib import Path

import uvloop
from dotenv import load_dotenv

## Begin: Add the project root to sys.path
project_root = Path(__file__).parent.parent.resolve()
sys.path.append(str(project_root))
print(f"Project root: {project_root}")


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
print("running uvloop as event loop policy for asyncio")

load_dotenv()
