import argparse
import os
import json
import sys
from scanner.file_scanner import scan_directory
from exporter.json_formatter import format_json
from config.settings_reader import ler_configuracoes
from config.configuration import iniciar_configuracao
from interface.menu import exibir_menu

def executar_com_argumentos():
    parser = argparse.ArgumentParser(description='Gera um JSON com a estrutura de arquivos.')
    parser.add_argument('--path', type=str, help='Caminho da pasta base a ser escaneada.')
    parser.add_argument('--output', type=str, help='Nome do arquivo de saída JSON.')
    parser.add_argument('--ignore', nargs='*', help='Lista de padrões de arquivos ou pastas a ignorar (ex: *.log temp*)')
    parser.add_argument('--ext', nargs='*', help='Lista de extensões de arquivos permitidas (ex: .pdf .txt .epub)')
    parser.add_argument('--config', action='store_true', help='Inicia configuração interativa.')

    args = parser.parse_args()

    # Se --config for passado, inicia o modo interativo e sai
    if args.config:
        iniciar_configuracao()
        return

    # Carregar configurações do arquivo, se existir
    config_padrao = ler_configuracoes()

    # Se o argumento for passado via CLI, ele tem prioridade. Se não, usa o do settings.conf. Se nem isso, usa valor padrão.
    base_path = os.path.abspath(args.path) if args.path else os.path.abspath(config_padrao.get("default_path", "."))
    output_file = args.output or config_padrao.get("default_output", "saida.json")
    ignore_list = args.ignore if args.ignore is not None else config_padrao.get("ignore", [])
    allowed_ext = args.ext if args.ext is not None else config_padrao.get("extensions", [])

    if not os.path.isdir(base_path):
        print(f"[Erro] O caminho '{base_path}' não é um diretório válido.")
        return

    print(f"[INFO] Escaneando a pasta: {base_path}")

    estrutura = {
        "secoes": scan_directory(
            path=base_path,
            ignore_list=ignore_list,
            allowed_extensions=allowed_ext
        )
    }

    resultado = format_json(estrutura)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print(f"[OK] JSON gerado em: {output_file}")

def main():
    while True:
        from cli.controller import continuar
        if not continuar():
            break

if __name__ == "__main__":
    main()

def foi_executado_com_argumentos():
    return len(sys.argv) > 1

def esta_rodando_como_exe():
    return getattr(sys, 'frozen', False)

def continuar():
    if foi_executado_com_argumentos():
        print("[Controller] Argumentos detectados. Executando modo CLI direto.\n")
        executar_com_argumentos()
        return False

    if esta_rodando_como_exe():
        print("[Controller] Modo .exe detectado. GUI será ativada (ainda em texto).\n")
        # Aqui futuramente chamaremos a GUI
        return False

    print("[Controller] Nenhum argumento. Entrando no menu interativo via terminal.\n")
    exibir_menu()
    return False
