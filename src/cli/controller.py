import argparse
import os
import json
import sys

from scanner.file_scanner import scan_directory
from exporter.json_formatter import format_json
from config.settings_reader import load_configurations
from config.cli.configuration import initialize_configuration
from interface.menu import display_main_menu
from interface.gui import show_gui_interface
from utils.logger import record_activity
from utils.context_manager import set_context, get_context, is_cli, is_gui

def execute_with_arguments():
    parser = argparse.ArgumentParser(description='Generates a json with the file structure.')
    parser.add_argument('--path', type=str, help='Path to the base folder to be scanned.')
    parser.add_argument('--output', type=str, help='Name of the output JSON file.')
    parser.add_argument('--ignore', nargs='*', help='List of file or folder patterns to ignore (ex: *.log temp*)')
    parser.add_argument('--ext', nargs='*', help='List of allowed file extensions (ex: .pdf .txt .epub)')
    parser.add_argument('--config', action='store_true', help='Starts interactive configuration.')

    args = parser.parse_args()
    record_activity(f"Arguments received: {sys.argv[1:]}", nivel="debug", local="controller")

    if args.config:
        record_activity("Interactive configuration requested via argument", nivel="info", local="controller")
        initialize_configuration()
        return

    default_config = load_configurations()
    if not default_config:
        print("[Erro] Não foi possível ler o arquivo de configuração. Iniciando configuração interativa.")
        initialize_configuration()

    base_path = os.path.abspath(args.path) if args.path else os.path.abspath(default_config.get("default_path", "."))
    output_file = args.output or default_config.get("default_output", "saida.json")
    ignore_list = args.ignore if args.ignore is not None else default_config.get("ignore", [])
    allowed_ext = args.ext if args.ext is not None else default_config.get("extensions", [])

    record_activity(f"Used Final Parameters- path: {base_path}, output: {output_file}, ignore: {ignore_list}, ext: {allowed_ext}", nivel="debug", local="controller")

    if not os.path.isdir(base_path):
        record_activity(f"Invalid path informed: {base_path}", nivel="error", local="controller")
        print(f"[Erro] O caminho '{base_path}' não é um diretório válido.")
        return

    record_activity(f"Starting scan: {base_path}", nivel="info", local="controller")
    directory_structure = {
        "secoes": scan_directory(
            path=base_path,
            ignore_list=ignore_list,
            allowed_extensions=allowed_ext
        )
    }

    json_output = format_json(directory_structure)

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_output, f, ensure_ascii=False, indent=2)
        record_activity(f"JSON file saved in: {output_file}", nivel="info", local="controller")
    except Exception as e:
        record_activity(f"Error saving JSON: {str(e)}", nivel="error", local="controller")
        record_activity(f"Context when failingsalvar: output={output_file}, estrutura={directory_structure}", nivel="debug", local="controller")

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
