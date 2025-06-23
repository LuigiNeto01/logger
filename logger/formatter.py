# formatters.py
import logging
import json
from datetime import datetime

# Importamos ColoredFormatter do colorlog para formatar mensagens com cor
from colorlog import ColoredFormatter

# Definimos um formatter colorido para console
def create_color_formatter() -> logging.Formatter:
    """Cria um formatter para console com cores para cada nível de log."""
    # Formato da mensagem incluindo cor e data
    fmt_str = "%(log_color)s%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    date_fmt = "%Y-%m-%d %H:%M:%S"
    # Mapeamento de cores para cada nível de log (inclui níveis customizados SUCCESS e FAIL)
    colors = {
        "DEBUG": "cyan",
        "INFO": "white",
        "SUCCESS": "green",    # nível de sucesso (personalizado) em verde
        "WARNING": "yellow",
        "ERROR": "red",
        "FAIL": "bold_red",   # nível de falha (personalizado) em vermelho forte
        "CRITICAL": "bold_red"
    }
    return ColoredFormatter(fmt_str, datefmt=date_fmt, log_colors=colors)

# Formatter para logs em JSON
class JsonLogFormatter(logging.Formatter):
    """Formatter que formata registros de log em JSON."""
    def format(self, record: logging.LogRecord) -> str:
        # Monta dicionário com campos desejados
        log_entry = {
            "timestamp": datetime.now().isoformat(sep=' ', timespec='seconds'),  # data/hora atual
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage()
        }
        # Se houver informação de exceção, inclui o traceback no JSON
        if record.exc_info:
            log_entry["traceback"] = self.formatException(record.exc_info)
        # Retorna o log como string JSON
        return json.dumps(log_entry, ensure_ascii=False)
