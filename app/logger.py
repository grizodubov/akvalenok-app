import logging
from datetime import datetime
from typing import Any

from pythonjsonlogger import jsonlogger

from app.config import settings

logger = logging.getLogger()

log_handler = logging.StreamHandler()


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(
            self,
            log_record: dict[str, Any],
            record: logging.LogRecord,
            message_dict: dict[str, Any],
    ) -> None:
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


formatter = CustomJsonFormatter(
    "%(timestamp)s %(level)s %(message)s %(module)s %(funcName)s"
)

log_handler.setFormatter(formatter)
logger.addHandler(log_handler)
logger.setLevel(settings.LOG_LEVEL)
