# logger/handlers.py

import logging, sys
from pathlib import Path
from .formatter import create_color_formatter, JsonLogFormatter  # importa do seu formatter.py
from . import config

class JsonArrayFileHandler(logging.FileHandler):
    """Handler que escreve um array JSON com vírgulas entre objetos."""
    def __init__(self, filename, mode='w', encoding=None, delay=False):
        super().__init__(filename, mode, encoding, delay)
        self._is_first = True
        # Quando não for delay, já escreve o '[' de abertura
        if not delay and self.stream:
            self.stream.write('[\n')

    def emit(self, record):
        try:
            msg = self.format(record)
            if self._is_first:
                self.stream.write(msg)
                self._is_first = False
            else:
                # escreve vírgula antes do próximo objeto
                self.stream.write(',\n' + msg)
            self.flush()
        except Exception:
            self.handleError(record)

    def close(self):
        # Fecha o array JSON
        try:
            self.stream.write('\n]\n')
        except Exception:
            pass
        super().close()

def setup_handlers(logger: logging.Logger) -> None:
    Path(config.LOG_DIR).mkdir(parents=True, exist_ok=True)

    # Console colorido
    if config.LOG_TO_CONSOLE:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(config.LOG_LEVEL)
        ch.setFormatter(create_color_formatter())
        logger.addHandler(ch)

    # Arquivo texto
    if config.LOG_TO_FILE:
        text_path = config.LOG_DIR / config.LOG_FILE_NAME
        fh = logging.FileHandler(text_path, mode='a', encoding='utf-8')
        fh.setLevel(config.LOG_LEVEL)
        fh.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))
        logger.addHandler(fh)

    # Arquivo JSON em array
    if config.LOG_TO_JSON:
        json_path = config.LOG_DIR / config.LOG_JSON_NAME
        jh = JsonArrayFileHandler(json_path, mode='w', encoding='utf-8')
        jh.setLevel(config.LOG_LEVEL)
        jh.setFormatter(JsonLogFormatter())
        logger.addHandler(jh)
