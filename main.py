# exemplo_de_uso.py
import asyncio
from logger.custom_logger import get_logger
from logger.validators    import monitor_internet
from logger.config import *

# Inicializa o logger customizado
logger = get_logger("rpa_app")

# Exemplos de logs
logger.info("Iniciando processo RPA...")
logger.success("Primeira etapa concluída com sucesso!")  # log de sucesso (verde no console)

print('sucesso')
