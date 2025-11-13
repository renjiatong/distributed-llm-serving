import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger("llm-serving")
logger.setLevel(logging.INFO)

log_handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()

log_handler.setFormatter(formatter)
logger.addHandler(log_handler)