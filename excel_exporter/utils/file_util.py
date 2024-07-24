from _datetime import datetime
import os
import shutil
import time
from typing import Optional

STORE_PATH = "storage"
CONFIG_PATH = "config"
OUTPUT_PATH = os.path.join("media", "excel_output")


def get_store_path(base_path: Optional[str] = None) -> str:
    store_path = OUTPUT_PATH if base_path is None else base_path
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S.%f")
    os.makedirs(os.path.join(store_path, timestamp), exist_ok=True)
    return os.path.join(store_path, timestamp)
