import asyncio
import sys
from pathlib import Path

import uvloop
from dotenv import load_dotenv

from services.admin_sdk import init_admin_sdk

### Begin: Add the project root to sys.path
# Calculate the path to the root of the project, assuming the script is in the 'streamlit' directory
project_root = Path(__file__).parent.parent.resolve()
# Add the project root to sys.path
sys.path.append(str(project_root))
### End: Add the project root to sys.path


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

print("running uvloop as the event loop policy for asyncio")

load_dotenv()
# init firebase admin sdk
init_admin_sdk()
