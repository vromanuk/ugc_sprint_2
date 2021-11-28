import logging

import uvicorn

from src.core.config import get_settings
from src.core.logger import LOGGING

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "src.main:app",
        host=settings.APPLICATION_HOST,
        port=settings.APPLICATION_PORT,
        log_config=LOGGING,
        log_level=getattr(logging, settings.LOG_LEVEL.upper()),
        access_log=False,
    )
