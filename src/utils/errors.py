import traceback
import os
import json

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt

from utils.context_manager import is_cli
from utils.logger import record_activity

def _emit_error(message, local, window=None):
    if is_cli():
        print(message)
        record_activity(message, log_level="error", log_origin=local)
    else:
        QMessageBox.warning(
            window,
            "Erro",
            message,
            QMessageBox.Ok,
        )
        record_activity(message, log_level="error", log_origin=local)

def show_simple_error(message, local):
    _emit_error(f"[ERRO] {message}", local)

def show_full_error(error, context="Erro"):
    _emit_error(f"[ERRO] {context}: {str(error)}")
    if is_cli():
        traceback.print_exc()

def validate_directory(path):
    if not os.path.isdir(path):
        return False
    return True

def validate_access(path):
    if not os.access(path, os.R_OK):
        return False
    return True


def validate_not_empty(value):
    if not value.strip():
        return False
    return True

def validate_file_name(value):
    if not value.isalnum() or not value:
        return False
    return True

def get_int_input(prompt, default=None):
    try:
        value = input(prompt)
        return True
    except ValueError:
        record_activity(f"Erro: valor inválido '{value}'.", log_level="error", log_origin="erro")


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

def exists_path(path):
    if not os.path.exists(path):
        return False
    return True
