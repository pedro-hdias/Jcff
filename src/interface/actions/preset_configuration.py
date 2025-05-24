import json
import os

from PySide6.QtWidgets import QMessageBox

from config.settings_reader import load_configurations
from config.gui.configuration import TelaConfiguracao
from scanner.file_scanner import scan_directory
from exporter.json_formatter import format_json
from utils import errors
from utils.logger import record_activity
from utils.speech import speech

def dialogo_informativo(title_window, message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    msg.setWindowTitle(title_window)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()

def executar_com_configuracao_salva():
    speech("Executando com configuração salva")
    config = load_configurations()
    if not config:
        record_activity("Nenhuma configuração salva encontrada.", nivel="warning", local="action")
        dialogo_informativo("Nenhuma configuração salva", "Nenhuma configuração salva encontrada. Por favor, configure primeiro.")
        return

    path = os.path.abspath(config.get("default_path", "."))
    output = config.get("default_output", "saida.json")
    ext = config.get("extensions", [])
    ignore = config.get("ignore", [])
    speech("Carregamento das configurações realizado. Iniciando validação das configurações.")

    record_activity(f"Executando com config salva - path: {path}, output: {output}, ext: {ext}, ignore: {ignore}", nivel="debug", local="menu")


    if not errors.validate_directory(path):
        record_activity(f"Caminho inválido na config: {path}", nivel="error", local="actions")
        errors.show_simple_error(f"[ERRO] Caminho inválido: {path}", "Actions")
        return

    speech("Iniciando escaneamento do diretório.")

    estrutura = {
        "secoes": scan_directory(path, ignore, ext)
    }

    with open(output, 'w', encoding='utf-8') as f:
        json.dump(format_json(estrutura), f, ensure_ascii=False, indent=2)

    record_activity(f"Arquivo JSON salvo com configuração salva em: {output}", nivel="info", local="actions")
    dialogo_informativo("Arquivo JSON Gerado", f"Arquivo JSON salvo em: {output}")

