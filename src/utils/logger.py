import os
from datetime import datetime
from utils.writer import write_json

EXECUTION_DATE = datetime.now().strftime("%Y-%m-%d")
EXECUTION_TIME = datetime.now().strftime("%H%M%S")
LOG_FILE_NAME = f"log-{EXECUTION_DATE.replace('-', '')}-{EXECUTION_TIME}.log"
LOGS_DIRECTORY = os.path.join(os.getcwd(), "logs")
LOG_FILE_PATH = os.path.join(LOGS_DIRECTORY, LOG_FILE_NAME)

log_data = {EXECUTION_DATE: []}

def record_activity(log_message, log_origin, log_level="info"):
    log_entry = {
        "level": log_level,
        "local": log_origin,
        "message": log_message,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    log_data[EXECUTION_DATE].append(log_entry)
    _persist_log()

def _persist_log():
    is_log_saved = write_json(LOG_FILE_PATH, log_data)
    if not is_log_saved:
        print("[LOGGER] Falha ao salvar o log usando writer.py")
