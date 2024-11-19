import os
import sys
from pathlib import Path

from dotenv import load_dotenv

project_root = Path(__file__).parent.parent.resolve()
sys.path.append(str(project_root))

if os.environ.get("ENV", "local") == "local":
    load_dotenv(dotenv_path="./.env.local")
else:
    load_dotenv()


def _local_init_admin_sdk():
    from src.services.admin_sdk import init_admin_sdk

    init_admin_sdk()


_local_init_admin_sdk()
