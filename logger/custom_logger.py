# app/custom_logger.py

import logging
import sys
import requests
import traceback
from datetime import datetime

from . import config
from .handlers import setup_handlers

# Níveis customizados
SUCCESS_LEVEL = 25
FAIL_LEVEL    = 45
logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")
logging.addLevelName(FAIL_LEVEL,    "FAIL")

class CustomLogger(logging.Logger):
    """Logger com .success(), .fail() e envio opcional para API de monitoramento."""

    def _send_to_api(self, level: int, msg: str, exc_info=None):
        """Se habilitado, faz POST do log JSON para a API."""
        if not config.MONITOR_API_ENABLED:
            return
        payload = {
            "timestamp": datetime.now().isoformat(sep=' ', timespec='seconds'),
            "level":   logging.getLevelName(level),
            "logger_name": self.name,
            "message": msg
        }
        if exc_info:
            payload["traceback"] = "".join(traceback.format_exception(*exc_info))
        try:
            requests.post(config.MONITOR_API_URL, json=payload, timeout=3)
        except Exception:
            # falha no envio não pode quebrar o app
            pass

    def debug(self, msg, *args, **kwargs):
        super().debug(msg, *args, **kwargs)
        self._send_to_api(logging.DEBUG, msg)

    def info(self, msg, *args, **kwargs):
        super().info(msg, *args, **kwargs)
        self._send_to_api(logging.INFO, msg)

    def warning(self, msg, *args, **kwargs):
        super().warning(msg, *args, **kwargs)
        self._send_to_api(logging.WARNING, msg)

    def error(self, msg, *args, **kwargs):
        exc = kwargs.get('exc_info')
        super().error(msg, *args, **kwargs)
        self._send_to_api(logging.ERROR, msg, exc_info=exc)

    def critical(self, msg, *args, **kwargs):
        exc = kwargs.get('exc_info')
        super().critical(msg, *args, **kwargs)
        self._send_to_api(logging.CRITICAL, msg, exc_info=exc)

    def success(self, msg: str, *args, **kwargs) -> None:
        """Nível SUCCESS (verde) e envio para API."""
        super().log(SUCCESS_LEVEL, msg, *args, **kwargs)
        self._send_to_api(SUCCESS_LEVEL, msg)

    def fail(self, msg: str, *args, exit_code: int = None, **kwargs) -> None:
        """Nível FAIL (vermelho), captura de traceback e envio para API."""
        exc = sys.exc_info()
        super().log(FAIL_LEVEL, msg, *args, exc_info=exc, **kwargs)
        self._send_to_api(FAIL_LEVEL, msg, exc_info=exc)

        # Sentry opcional (se configurado)
        if config.USE_SENTRY:
            try:
                import sentry_sdk
                sentry_sdk.capture_exception()
            except ImportError:
                pass

        # Encerra o processo se configurado
        if config.STOP_ON_FAIL:
            logging.shutdown()
            code = exit_code if exit_code is not None else config.FAIL_EXIT_CODE
            sys.exit(code)

# Registra a classe custom como padrão
logging.setLoggerClass(CustomLogger)

def get_logger(name: str = "RPA") -> CustomLogger:
    logger = logging.getLogger(name)
    logger.setLevel(config.LOG_LEVEL)
    setup_handlers(logger)
    return logger
