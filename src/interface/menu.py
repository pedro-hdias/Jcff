import json
import os

from config.settings_reader import load_configurations
from config.cli.configuration import initialize_configuration
from scanner.file_scanner import scan_directory
from exporter.json_formatter import format_json
from utils import errors
from utils.logger import record_activity

def display_main_menu():
    record_activity("Interactive Menu Started", nivel="info", local="menu")
    while True:
        print("\n===== MENU PRINCIPAL =====")
        print("1 - Executar com configuração salva")
        print("2 - Executar com valores personalizados")
        print("3 - Ver configuração salva")
        print("4 - Configurar")
        print("5 - Sair")

        menu_option = input("Escolha uma opção: ").strip()
        if not errors.validate_not_empty(menu_option) and not errors.get_int_input(menu_option):
            record_activity(f"Input received in the menu: {menu_option}", nivel="debug", local="menu")
            errors.show_simple_error("Invalid option. Enter a number between 1 and 5.")
        record_activity(f"Input received in the menu: {menu_option}", nivel="debug", local="menu")

        match menu_option:
            case "1":
                record_activity("Option 1 selected: Executar com configuração salva", nivel="info", local="menu")
                execute_with_saved_config()
            case "2":
                record_activity("Option 2 selected: Executar com valores personalizados", nivel="info", local="menu")
                run_with_custom_values()
            case "3":
                record_activity("Option 3 selected: mostrar configurações salvas", nivel="info", local="menu")
                show_saved_settings()
            case "4":
                record_activity("Option 4 selected: iniciar configuração interativa", nivel="info", local="menu")
                initialize_configuration()
            case "5":
                record_activity("Opção 5 selecionada: sair do programa", nivel="info", local="menu")
                print("Encerrando...\n")
                return
            case _:
                record_activity(f"Invalid option: {menu_option}", nivel="warning", local="menu")
                print("Opção inválida.")

def execute_with_saved_config():
    config = load_configurations()

    path = os.path.abspath(config.get("default_path", "."))
    output = config.get("default_output", "saida.json")
    ext = config.get("extensions", [])
    ignore = config.get("ignore", [])

    record_activity(f"Running with loaded settings - path: {path}, output: {output}, ext: {ext}, ignore: {ignore}", nivel="debug", local="menu")

    if not errors.validate_directory(path):
        record_activity(f"Invalid path at settings: {path}", nivel="error", local="menu")
        print(f"[ERRO] Caminho inválido: {path}")
        return

    json_output = {
        "secoes": scan_directory(path, ignore, ext)
    }

    with open(output, 'w', encoding='utf-8') as f:
        json.dump(format_json(json_output), f, ensure_ascii=False, indent=2)

    record_activity(f"Json file saved with saved configuration in: {output}", nivel="info", local="menu")
    print(f"Arquivo salvo em: {output}")

def run_with_custom_values():
    path = input("Caminho para escanear: ").strip()
    output = input("Nome do arquivo de saída: ").strip() or "saida.json"
    ext = input("Extensões permitidas (.pdf,.txt,...): ").strip().split(",")
    ignore = input("Padrões a ignorar (*.log,temp*,...): ").strip().split(",")

    ext = [e.strip() for e in ext if e.strip()]
    ignore = [i.strip() for i in ignore if i.strip()]
    path = os.path.abspath(path)

    record_activity(f"Personalization - path: {path}, output: {output}, ext: {ext}, ignore: {ignore}", nivel="debug", local="menu")

    if not os.path.isdir(path):
        record_activity(f"Invalid path informed in personalization: {path}", nivel="error", local="menu")
        print(f"[ERRO] Caminho inválido: {path}")
        return

    json_output = {
        "secoes": scan_directory(path, ignore, ext)
    }

    with open(output, 'w', encoding='utf-8') as f:
        json.dump(format_json(json_output), f, ensure_ascii=False, indent=2)

    record_activity(f"JSON File saved with custom parameters in: {output}", nivel="info", local="menu")
    print(f"Arquivo salvo em: {output}")

def show_saved_settings():
    loaded_config = load_configurations()
    record_activity(f"Showing Save Configuration: {loaded_config}", nivel="debug", local="menu")
    print("\n===== CONFIGURAÇÃO SALVA =====")
    for chave, valor in loaded_config.items():
        print(f"{chave}: {valor}")
