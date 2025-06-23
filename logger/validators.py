# logger/validators.py
import asyncio
import logging
import sys
import urllib.request

from . import config

async def check_internet() -> bool:
    try:
        urllib.request.urlopen("http://www.google.com", timeout=5)
        return True
    except Exception:
        logging.critical("Conexão com a Internet perdida! 🌐", exc_info=True)
        if config.STOP_ON_FAIL:
            logging.shutdown()
            sys.exit(config.FAIL_EXIT_CODE)
        return False

async def monitor_internet(interval: int = 10):
    while True:
        await check_internet()
        await asyncio.sleep(interval)
