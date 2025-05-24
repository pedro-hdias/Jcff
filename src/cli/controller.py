import argparse
import os
import json
import sys

from scanner.file_scanner import scan_directory
from exporter.json_formatter import format_json
from config.settings_reader import ler_configuracoes
from config.cli.configuration import iniciar_configuracao
from interface.menu import display_main_menu
from interface.gui import show_gui_interface
from utils.logger import record_activity
from utils.context_manager import set_context, get_context, is_cli, is_gui

def execute_with_arguments():
    parser = argparse.ArgumentParser(description='Gera um JSON com a estrutura de arquivos.')
    parser.add_argument('--path', type=str, help='Caminho da pasta base a ser escaneada.')
    parser.add_argument('--output', type=str, help='Nome do arquivo de saída JSON.')
    parser.add_argument('--ignore', nargs='*', help='Lista de padrões de arquivos ou pastas a ignorar (ex: *.log temp*)')
    parser.add_argument('--ext', nargs='*', help='Lista de extensões de arquivos permitidas (ex: .pdf .txt .epub)')
    parser.add_argument('--config', action='store_true', help='Inicia configuração interativa.')

    args = parser.parse_args()
    record_activity(f"Argumentos recebidos: {sys.argv[1:]}", nivel="debug", local="controller")

    if args.config:
        record_activity("Configuração interativa solicitada via argumento", nivel="info", local="controller")
        iniciar_configuracao()
        return

    config_padrao = ler_configuracoes()
    if not config_padrao:
        print("[Erro] Não foi possível ler o arquivo de configuração. Iniciando configuração interativa.")
        iniciar_configuracao()

    base_path = os.path.abspath(args.path) if args.path else os.path.abspath(config_padrao.get("default_path", "."))
    output_file = args.output or config_padrao.get("default_output", "saida.json")
    ignore_list = args.ignore if args.ignore is not None else config_padrao.get("ignore", [])
    allowed_ext = args.ext if args.ext is not None else config_padrao.get("extensions", [])

    record_activity(f"Parâmetros finais usados - path: {base_path}, output: {output_file}, ignore: {ignore_list}, ext: {allowed_ext}", nivel="debug", local="controller")

    if not os.path.isdir(base_path):
        record_activity(f"Caminho inválido informado: {base_path}", nivel="error", local="controller")
        print(f"[Erro] O caminho '{base_path}' não é um diretório válido.")
        return

    record_activity(f"Iniciando varredura no caminho: {base_path}", nivel="info", local="controller")
    estrutura = {
        "secoes": scan_directory(
            path=base_path,
            ignore_list=ignore_list,
            allowed_extensions=allowed_ext
        )
    }

    resultado = format_json(estrutura)

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)
        record_activity(f"Arquivo JSON salvo em: {output_file}", nivel="info", local="controller")
    except Exception as e:
        record_activity(f"Erro ao salvar JSON: {str(e)}", nivel="error", local="controller")
        record_activity(f"Contexto ao falhar salvar: output={output_file}, estrutura={estrutura}", nivel="debug", local="controller")

def is_executed_with_args():
    return len(sys.argv) > 1

def is_executable_context():
    return getattr(sys, 'frozen', False)

def initialize_context():
    if is_executable_context():
        set_context("gui")
    else:
        set_context("cli")

    record_activity(f"Context defined as: {get_context().upper()}", nivel="info", local="controller")

    if is_executed_with_args():
        record_activity("Arguments detected. Executing direct CLI mode.", nivel="info", local="controller")
        execute_with_arguments()
        return False

    if is_gui():
        record_activity("Mode .exe detected. Gui will be activated.", nivel="info", local="controller")
        show_gui_interface()
        return False

    record_activity("No arguments detected. Entering interactive menu via terminal.", nivel="info", local="controller")
    display_main_menu()
    return False
