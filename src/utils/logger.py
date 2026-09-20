"""
Logging Ultilities

Responsibilities:
- Configure loggers from console and file output.
- Ensure consistent formatting and log level across modules.
"""

import logging
from src.utils.config import BASE_DIR
from src.utils.config import LOG_LEVEL

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

def get_logger(name:str):
    """
    Create and configure a logger with console and file handlers. 

    Parameters:
    -----------
    name: str
        Name of the logger, typically class or module name.

    Returns:
    --------
    logging.Logger
        Configured logger instance with timestamped console and file output.
    """

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # Avoid adding duplicate handlers if logger is already configured
    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # File handler
        file_handler = logging.FileHandler(LOG_DIR/'app.log')
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
    return logger        