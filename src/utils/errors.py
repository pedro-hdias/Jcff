import traceback
import os
import json
from utils.context_manager import is_cli


def _emit_error(message):
    if is_cli():
        print(message)
    else:
        from utils import logger  # futuro logger.py
        logger.registrar(message, nivel="erro")


def show_simple_error(error, context="Erro"):
    _emit_error(f"[ERRO] {context}: {str(error)}")


def show_full_error(error, context="Erro"):
    _emit_error(f"[ERRO] {context}: {str(error)}")
    if is_cli():
        traceback.print_exc()


def validate_directory(path):
    if not os.path.isdir(path):
        raise ValueError(f"O caminho '{path}' não é um diretório válido.")


def validate_access(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"O caminho '{path}' não existe.")
    if not os.access(path, os.R_OK):
        raise PermissionError(f"Sem permissão para acessar '{path}'.")


def validate_not_empty(value, label="valor"):
    if not value.strip():
        raise ValueError(f"O {label} não pode ser vazio.")


def get_int_input(prompt, default=None):
    try:
        value = input(prompt)
        return int(value)
    except ValueError:
        raise ValueError("Valor numérico inválido.")


def safe_json_write(path, data):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        show_simple_error(e, f"Falha ao salvar o JSON em '{path}'")
        return False


def safe_listdir(path):
    try:
        return sorted(os.listdir(path))
    except Exception as e:
        show_simple_error(e, f"Erro ao listar o diretório '{path}'")
        return []
