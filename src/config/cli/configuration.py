import os
from configparser import ConfigParser
from config.settings_writer import save_configuration
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
    record_activity(f"Nome do arquivo recebido: {output}", log_level="debug", log_origin="configuration")
    while not errors.validate_not_empty(output) and not errors.validate_file_name(output):
        errors.show_simple_error(f"O nome '{output}' não é válido.", "configuration")
        _set_output_file()
    return f"{output}.json"

def initialize_configuration():
    print("🔧 Iniciando configuração interativa:\n")

    path = _set_path()
    record_activity(f"Standard path: {path}", log_level="debug", log_origin="configuration")

    output = _set_output_file()
    record_activity(f"Output file name: {output}", log_level="debug", log_origin="configuration")

    allowed_extensions = input("Allowed extensions separated by comma (ex: .pdf,.epub,.txt) [Enter for none]: ").strip()
    if allowed_extensions:
        allowed_extensions = [ext.strip() for ext in allowed_extensions.split(",")]
        record_activity(f"allowed extensions: {allowed_extensions}", log_level="debug", log_origin="configuration")
    else:
        allowed_extensions = []
        record_activity("No specified extensions", log_level="debug", log_origin="configuration")

    ignore_patterns = input("Padrões a ignorar separados por vírgula (ex: *.log,temp*,__pycache__) [Enter para nenhum]: ").strip()
    if ignore_patterns:
        ignore_patterns = [p.strip() for p in ignore_patterns.split(",")]
        record_activity(f"patterns to ignore: {ignore_patterns}", log_level="debug", log_origin="configuration")
    else:
        ignore_patterns = []
        record_activity("No pattern to ignore defined", log_level="debug", log_origin="configuration")

    configuration_settings = {
        "default_path": path,
        "default_output": output,
        "extensions": allowed_extensions,
        "ignore": ignore_patterns
    }

    save_configuration(configuration_settings)
    print("\n✅ Arquivo de configuração criado com sucesso!")

if __name__ == "__main__":
    initialize_configuration()
