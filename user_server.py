import uvicorn
import logging
from logging.handlers import TimedRotatingFileHandler

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "logformatter": {
            "format": "[%(asctime)s.%(msecs)03d] %(levelname)s [%(thread)d] - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "logfile": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "logformatter",
            "filename": "log/log_user",
            "when": "midnight",
            "backupCount": 7,  # Optional, number of backup files to keep
        },
        "logconsole": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "logformatter",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": ["logfile", "logconsole"],
        },
    },
}

if __name__ == "__main__":
    uvicorn.run(
        "server.vital.service.UserService:userService",
        host="0.0.0.0",
        port=3000,
        reload=True,
        workers=4,
        log_config=log_config
    )