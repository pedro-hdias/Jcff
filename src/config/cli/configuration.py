import os
from configparser import ConfigParser
from config.settings_writer import salvar_configuracoes
from utils import errors
from utils.logger import record_activity

def _set_path():
    """
    Define o caminho padrão para o arquivo de configuração.
    Se o caminho não for válido, solicita ao usuário um novo caminho.
    """
    path = input("Digite um caminho de diretório válido, por exemplo: C:/Users/SeuUsuario/Documentos/\n")
    while not errors.validate_not_empty(path) and not errors.exists_path(path) and not errors.validate_access(path) and not errors.validate_directory(path):
        errors.show_simple_error(f"O caminho '{path}' não é um diretório válido.", "configuration")
        _set_path()
    return path

def _set_output_file():
    """
    Define o nome do arquivo de saída.
    Se o nome não for válido, solicita ao usuário um novo nome.
    """
    output = input("Digite o nome do arquivo de saída (sem extensão): ").strip()
    record_activity(f"Nome do arquivo recebido: {output}", nivel="debug", local="configuration")
    while not errors.validate_not_empty(output) and not errors.validate_file_name(output):
        errors.show_simple_error(f"O nome '{output}' não é válido.", "configuration")
        _set_output_file()
    return f"{output}.json"

def iniciar_configuracao():
    print("🔧 Iniciando configuração interativa:\n")

    path = _set_path()
    record_activity(f"Caminho padrão: {path}", nivel="debug", local="configuration")

    output = _set_output_file()
    record_activity(f"Nome do arquivo de saída: {output}", nivel="debug", local="configuration")

    extensoes = input("Extensões permitidas separadas por vírgula (ex: .pdf,.epub,.txt) [Enter para nenhuma]: ").strip()
    if extensoes:
        extensoes = [ext.strip() for ext in extensoes.split(",")]
        record_activity(f"Extensões permitidas: {extensoes}", nivel="debug", local="configuration")
    else:
        extensoes = []
        record_activity("Nenhuma extensão permitida definida", nivel="debug", local="configuration")

    ignorar = input("Padrões a ignorar separados por vírgula (ex: *.log,temp*,__pycache__) [Enter para nenhum]: ").strip()
    if ignorar:
        ignorar = [p.strip() for p in ignorar.split(",")]
        record_activity(f"Padrões a ignorar: {ignorar}", nivel="debug", local="configuration")
    else:
        ignorar = []
        record_activity("Nenhum padrão a ignorar definido", nivel="debug", local="configuration")

    configuracoes = {
        "default_path": path,
        "default_output": output,
        "extensions": extensoes,
        "ignore": ignorar
    }

    salvar_configuracoes(configuracoes)
    print("\n✅ Arquivo de configuração criado com sucesso!")

if __name__ == "__main__":
    iniciar_configuracao()
