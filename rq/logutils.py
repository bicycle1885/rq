import logging
from logging.config import fileConfig

# Make sure that dictConfig is available
# This was added in Python 2.7/3.2
try:
    from logging.config import dictConfig
except ImportError:
    from rq.compat.dictconfig import dictConfig  # noqa

# whether log handlers have been already configured or not
_configured = False


def setup_loghandlers(level=None, config_file=None):
    global _configured

    if not _configured:
        if config_file:
            fileConfig(config_file, disable_existing_loggers=False)
        else:
            dictConfig({
                "version": 1,
                "disable_existing_loggers": False,

                "formatters": {
                    "console": {
                        "format": "%(asctime)s %(message)s",
                        "datefmt": "%H:%M:%S",
                    },
                },

                "handlers": {
                    "console": {
                        "level": "DEBUG",
                        #"class": "logging.StreamHandler",
                        "class": "rq.utils.ColorizingStreamHandler",
                        "formatter": "console",
                        "exclude": ["%(asctime)s"],
                    },
                },

                "root": {
                    "handlers": ["console"],
                    "level": "INFO",
                }
            })

        if level:
            root = logging.getLogger()
            root.setLevel(level)

        _configured = True
