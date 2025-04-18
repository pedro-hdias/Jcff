import argparse
import os
import json
import sys

from scanner.file_scanner import scan_directory
from exporter.json_formatter import format_json
from config.settings_reader import ler_configuracoes
from config.cli.configuration import iniciar_configuracao
from interface.menu import exibir_menu
from interface.gui import exibir_interface
from utils.logger import registrar
from utils.context_manager import set_context, get_context, is_cli, is_gui

def executar_com_argumentos():
    parser = argparse.ArgumentParser(description='Gera um JSON com a estrutura de arquivos.')
    parser.add_argument('--path', type=str, help='Caminho da pasta base a ser escaneada.')
    parser.add_argument('--output', type=str, help='Nome do arquivo de saída JSON.')
    parser.add_argument('--ignore', nargs='*', help='Lista de padrões de arquivos ou pastas a ignorar (ex: *.log temp*)')
    parser.add_argument('--ext', nargs='*', help='Lista de extensões de arquivos permitidas (ex: .pdf .txt .epub)')
    parser.add_argument('--config', action='store_true', help='Inicia configuração interativa.')

    args = parser.parse_args()
    registrar(f"Argumentos recebidos: {sys.argv[1:]}", nivel="debug", local="controller")

    if args.config:
        registrar("Configuração interativa solicitada via argumento", nivel="info", local="controller")
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

    registrar(f"Parâmetros finais usados - path: {base_path}, output: {output_file}, ignore: {ignore_list}, ext: {allowed_ext}", nivel="debug", local="controller")

    if not os.path.isdir(base_path):
        registrar(f"Caminho inválido informado: {base_path}", nivel="error", local="controller")
        print(f"[Erro] O caminho '{base_path}' não é um diretório válido.")
        return

    registrar(f"Iniciando varredura no caminho: {base_path}", nivel="info", local="controller")
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
        registrar(f"Arquivo JSON salvo em: {output_file}", nivel="info", local="controller")
    except Exception as e:
        registrar(f"Erro ao salvar JSON: {str(e)}", nivel="error", local="controller")
        registrar(f"Contexto ao falhar salvar: output={output_file}, estrutura={estrutura}", nivel="debug", local="controller")

def foi_executado_com_argumentos():
    return len(sys.argv) > 1

def esta_rodando_como_exe():
    return getattr(sys, 'frozen', False)

def continuar():
    if esta_rodando_como_exe():
        set_context("gui")
    else:
        set_context("cli")

    registrar(f"Contexto definido como: {get_context().upper()}", nivel="info", local="controller")

    if foi_executado_com_argumentos():
        registrar("Argumentos detectados. Executando modo CLI direto.", nivel="info", local="controller")
        executar_com_argumentos()
        return False

    if is_gui():
        registrar("Modo .exe detectado. GUI será ativada.", nivel="info", local="controller")
        exibir_interface()
        return False

    registrar("Nenhum argumento detectado. Entrando no menu interativo via terminal.", nivel="info", local="controller")
    exibir_menu()
    return False
