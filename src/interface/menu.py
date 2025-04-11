import json
import os

from config.settings_reader import ler_configuracoes
from config.configuration import iniciar_configuracao
from scanner.file_scanner import scan_directory
from exporter.json_formatter import format_json
from utils import errors
from utils.logger import registrar

def exibir_menu():
    registrar("Menu interativo iniciado", nivel="info", local="menu")
    while True:
        print("\n===== MENU PRINCIPAL =====")
        print("1 - Executar com configuração salva")
        print("2 - Executar com valores personalizados")
        print("3 - Ver configuração salva")
        print("4 - Configurar")
        print("5 - Sair")

        opcao = input("Escolha uma opção: ").strip()
        if not errors.validate_not_empty(opcao) and not errors.get_int_input(opcao):
            registrar(f"Input recebido no menu: {opcao}", nivel="debug", local="menu")
            errors.show_simple_error("Opção inválida. Digite um número entre 1 e 5.")
        registrar(f"Input recebido no menu: {opcao}", nivel="debug", local="menu")

        match opcao:
            case "1":
                registrar("Opção 1 selecionada: executar com configuração salva", nivel="info", local="menu")
                executar_com_configuracao_salva()
            case "2":
                registrar("Opção 2 selecionada: executar com valores personalizados", nivel="info", local="menu")
                executar_com_personalizacao()
            case "3":
                registrar("Opção 3 selecionada: ver configuração salva", nivel="info", local="menu")
                exibir_configuracao_salva()
            case "4":
                registrar("Opção 4 selecionada: iniciar configuração interativa", nivel="info", local="menu")
                iniciar_configuracao()
            case "5":
                registrar("Opção 5 selecionada: sair do programa", nivel="info", local="menu")
                print("Encerrando...\n")
                return
            case _:
                registrar(f"Opção inválida: {opcao}", nivel="warning", local="menu")
                print("Opção inválida.")

def executar_com_configuracao_salva():
    config = ler_configuracoes()

    path = os.path.abspath(config.get("default_path", "."))
    output = config.get("default_output", "saida.json")
    ext = config.get("extensions", [])
    ignore = config.get("ignore", [])

    registrar(f"Executando com config salva - path: {path}, output: {output}, ext: {ext}, ignore: {ignore}", nivel="debug", local="menu")

    if not errors.validate_directory(path):
        registrar(f"Caminho inválido na config: {path}", nivel="error", local="menu")
        print(f"[ERRO] Caminho inválido: {path}")
        return

    estrutura = {
        "secoes": scan_directory(path, ignore, ext)
    }

    with open(output, 'w', encoding='utf-8') as f:
        json.dump(format_json(estrutura), f, ensure_ascii=False, indent=2)

    registrar(f"Arquivo JSON salvo com configuração salva em: {output}", nivel="info", local="menu")
    print(f"Arquivo salvo em: {output}")

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
