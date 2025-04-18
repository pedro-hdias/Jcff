import json
import os

from PySide6.QtWidgets import QMessageBox

from config.settings_reader import ler_configuracoes
from config.gui.configuration import TelaConfiguracao
from scanner.file_scanner import scan_directory
from exporter.json_formatter import format_json
from utils import errors
from utils.logger import registrar
from utils.speech import speech

def dialogo_informativo(title_window, message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    msg.setWindowTitle(title_window)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()

def executar_com_configuracao_salva():
    speech("Executando com configuração salva")
    config = ler_configuracoes()
    if not config:
        registrar("Nenhuma configuração salva encontrada. Iniciando configuração interativa.", nivel="warning", local="menu")
        iniciar_configuracao()

    path = os.path.abspath(config.get("default_path", "."))
    output = config.get("default_output", "saida.json")
    ext = config.get("extensions", [])
    ignore = config.get("ignore", [])
    speech("Carregamento das configurações realizado. Iniciando validação das configurações.")

    registrar(f"Executando com config salva - path: {path}, output: {output}, ext: {ext}, ignore: {ignore}", nivel="debug", local="menu")


    if not errors.validate_directory(path):
        registrar(f"Caminho inválido na config: {path}", nivel="error", local="menu")
        errors.show_simple_error(f"[ERRO] Caminho inválido: {path}", "Actions")
        return

    speech("Iniciando escaneamento do diretório.")

    estrutura = {
        "secoes": scan_directory(path, ignore, ext)
    }

    with open(output, 'w', encoding='utf-8') as f:
        json.dump(format_json(estrutura), f, ensure_ascii=False, indent=2)

    registrar(f"Arquivo JSON salvo com configuração salva em: {output}", nivel="info", local="menu")
    dialogo_informativo("Arquivo JSON Gerado", f"Arquivo JSON salvo em: {output}")

def executar_com_personalizacao():
    path = input("Caminho para escanear: ").strip()
    output = input("Nome do arquivo de saída: ").strip() or "saida.json"
    ext = input("Extensões permitidas (.pdf,.txt,...): ").strip().split(",")
    ignore = input("Padrões a ignorar (*.log,temp*,...): ").strip().split(",")

    ext = [e.strip() for e in ext if e.strip()]
    ignore = [i.strip() for i in ignore if i.strip()]
    path = os.path.abspath(path)

    registrar(f"Personalização - path: {path}, output: {output}, ext: {ext}, ignore: {ignore}", nivel="debug", local="menu")

    if not os.path.isdir(path):
        registrar(f"Caminho inválido informado na personalização: {path}", nivel="error", local="menu")
        print(f"[ERRO] Caminho inválido: {path}")
        return

    estrutura = {
        "secoes": scan_directory(path, ignore, ext)
    }

    with open(output, 'w', encoding='utf-8') as f:
        json.dump(format_json(estrutura), f, ensure_ascii=False, indent=2)

    registrar(f"Arquivo JSON salvo com parâmetros personalizados em: {output}", nivel="info", local="menu")
    print(f"Arquivo salvo em: {output}")

def exibir_configuracao_salva():
    config = ler_configuracoes()
    registrar(f"Exibindo configuração salva: {config}", nivel="debug", local="menu")
    print("\n===== CONFIGURAÇÃO SALVA =====")
    for chave, valor in config.items():
        print(f"{chave}: {valor}")
