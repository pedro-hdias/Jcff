from config.settings_reader import ler_configuracoes
from config.configuration import iniciar_configuracao
from scanner.file_scanner import scan_directory
from exporter.json_formatter import format_json
import json
import os

def exibir_menu():
    while True:
        print("\n===== MENU PRINCIPAL =====")
        print("1 - Executar com configuração salva")
        print("2 - Executar com valores personalizados")
        print("3 - Ver configuração salva")
        print("4 - Configurar")
        print("5 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        match opcao:
            case "1":
                executar_com_configuracao_salva()
            case "2":
                executar_com_personalizacao()
            case "3":
                exibir_configuracao_salva()
            case "4":
                iniciar_configuracao()
            case "5":
                print("Encerrando...\n")
                return
            case _:
                print("Opção inválida.")

def executar_com_configuracao_salva():
    config = ler_configuracoes()

    path = os.path.abspath(config.get("default_path", "."))
    output = config.get("default_output", "saida.json")
    ext = config.get("extensions", [])
    ignore = config.get("ignore", [])

    if not os.path.isdir(path):
        print(f"[ERRO] Caminho inválido: {path}")
        return

    print(f"[INFO] Escaneando {path} com configurações salvas...")
    estrutura = {
        "secoes": scan_directory(path, ignore, ext)
    }

    with open(output, 'w', encoding='utf-8') as f:
        json.dump(format_json(estrutura), f, ensure_ascii=False, indent=2)

    print(f"[OK] JSON salvo em {output}")

def executar_com_personalizacao():
    path = input("Caminho para escanear: ").strip()
    output = input("Nome do arquivo de saída: ").strip() or "saida.json"
    ext = input("Extensões permitidas (por exemplo: .pdf,.txt): ").strip().split(",")
    ignore = input("Padrões a ignorar (por exemplo: *.log,temp*): ").strip().split(",")

    path = os.path.abspath(path)
    ext = [e.strip() for e in ext if e.strip()]
    ignore = [i.strip() for i in ignore if i.strip()]

    if not os.path.isdir(path):
        print(f"[ERRO] Caminho inválido: {path}")
        return

    print(f"[INFO] Escaneando {path} com parâmetros personalizados...")
    estrutura = {
        "secoes": scan_directory(path, ignore, ext)
    }

    with open(output, 'w', encoding='utf-8') as f:
        json.dump(format_json(estrutura), f, ensure_ascii=False, indent=2)

    print(f"[OK] JSON salvo em {output}")

def exibir_configuracao_salva():
    config = ler_configuracoes()
    print("\n===== CONFIGURAÇÃO SALVA =====")
    for chave, valor in config.items():
        print(f"{chave}: {valor}")
