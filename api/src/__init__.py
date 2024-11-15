import asyncio
import os

import uvloop
from dotenv import load_dotenv

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
print("running uvloop as event loop policy for asyncio")


if os.environ.get("ENV", "local") == "local":
    load_dotenv(dotenv_path="./.env.local")
else:
    load_dotenv()
