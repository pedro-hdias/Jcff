import os
from datetime import datetime
from utils.writer import write_json

# Preparar dados iniciais de execução
DATA_EXECUCAO = datetime.now().strftime("%Y-%m-%d")
HORA_EXECUCAO = datetime.now().strftime("%H%M%S")
NOME_ARQUIVO_LOG = f"log-{DATA_EXECUCAO.replace('-', '')}-{HORA_EXECUCAO}.log"
PASTA_LOG = os.path.join(os.getcwd(), "logs")
CAMINHO_LOG = os.path.join(PASTA_LOG, NOME_ARQUIVO_LOG)

# Estrutura base do log
log_data = {DATA_EXECUCAO: []}

def record_activity(mensagem, nivel="info", local="sistema"):
    entrada = {
        "level": nivel,
        "local": local,
        "message": mensagem,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    log_data[DATA_EXECUCAO].append(entrada)
    _salvar_log()

def _salvar_log():
    sucesso = write_json(CAMINHO_LOG, log_data)
    if not sucesso:
        print("[LOGGER] Falha ao salvar o log usando writer.py")
