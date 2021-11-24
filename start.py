import logging

import uvicorn

from src.core.config import get_settings
from src.core.logger import LOGGING

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=5000,
        log_config=LOGGING,
        log_level=getattr(logging, settings.LOG_LEVEL.upper()),
        access_log=False,
    )
