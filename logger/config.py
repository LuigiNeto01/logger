# config.py
import logging
from pathlib import Path

ROTA_API = "http://localhost:8000/"

# Quando True, cada log enviado localmente também será POSTado na sua API
MONITOR_API_ENABLED: bool = False  

# URL completa do endpoint de ingestão de logs da API de monitoramento
# ex: "http://localhost:8000/logs"
MONITOR_API_URL: str = f"{ROTA_API}logs"

# Pasta onde os arquivos de log serão armazenados
LOG_DIR: Path = Path("logs")

# Nível mínimo de severidade para registrar (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL: int = logging.DEBUG

# Opções de destino de log
LOG_TO_CONSOLE: bool = True      # Habilita saída de log no console (com cor)
LOG_TO_FILE: bool = True         # Habilita log em arquivo .log (texto plano)
LOG_TO_JSON: bool = True        # Habilita log em arquivo .json (formato JSON estruturado)

# Nomes de arquivo de log (dentro de LOG_DIR)
LOG_FILE_NAME: str = "app.log"
LOG_JSON_NAME: str = "app.json"

# Comportamentos do logger
STOP_ON_FAIL: bool = True        # Se True, o logger.fail() encerra a execução do script
FAIL_EXIT_CODE: int = 1          # Código de saída usado ao encerrar no fail (personalizável)

# Emissão de eventos (opcional)
EMIT_SUCCESS_EVENT: bool = False # Se True, emite evento ao chamar logger.success()
EMIT_FAIL_EVENT: bool = False    # Se True, emite evento ao chamar logger.fail()

# Callbacks de evento (se necessário, para integração com sistema de eventos do RPA)
SUCCESS_EVENT_CALLBACK = None    # Ex: função a ser chamada em success (pode ser definido pelo usuário)
FAIL_EVENT_CALLBACK = None       # Ex: função a ser chamada em fail
