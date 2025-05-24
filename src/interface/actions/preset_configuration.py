import json
import os

from PySide6.QtWidgets import QMessageBox

from config.settings_reader import load_configurations
from config.gui.configuration import ConfigurationDialog
from scanner.file_scanner import scan_directory
from exporter.json_formatter import format_json
from utils import errors
from utils.logger import record_activity
from utils.speech import speech

def show_information_dialog(dialog_title, dialog_message):
    information_dialog = QMessageBox()
    information_dialog.setIcon(QMessageBox.Information)
    information_dialog.setText(dialog_message)
    information_dialog.setWindowTitle(dialog_title)
    information_dialog.setStandardButtons(QMessageBox.Ok)
    information_dialog.exec()

def run_with_preset_config():
    speech("Executando com configuração salva")
    preset_configuration = load_configurations()
    if not preset_configuration:
        record_activity("No saved configuration found.", nivel="warning", local="action")
        show_information_dialog(
            "Nenhuma configuração salva",
            "Nenhuma configuração salva encontrada. Por favor, configure primeiro."
        )
        return

    path = os.path.abspath(preset_configuration.get("default_path", "."))
    output = preset_configuration.get("default_output", "saida.json")
    ext = preset_configuration.get("extensions", [])
    ignore = preset_configuration.get("ignore", [])
    speech("Carregamento das configurações realizado. Iniciando validação;")

    record_activity(
        f"Running with saved settings - path: {path}, output: {output}, ext: {ext}, ignore: {ignore}", 
        nivel="debug", local="menu"
    )

    if not errors.validate_directory(path):
        record_activity(
            f"Invalid path at Config: {path}", nivel="error", local="actions"
        )
        errors.show_simple_error(f"[ERRO] Caminho inválido: {path}", "Actions")
        return

    speech("Iniciando escaneamento do diretório.")

    json_output = {
        "secoes": scan_directory(path, ignore, ext)
    }

    with open(output, 'w', encoding='utf-8') as f:
        json.dump(format_json(json_output), f, ensure_ascii=False, indent=2)

    record_activity(
        f"Json file saved with saved configuration in: {output}", nivel="info", local="actions"
    )
    show_information_dialog("Arquivo JSON Gerado", f"Arquivo JSON salvo em: {output}")
