import os
from configparser import ConfigParser
from utils import errors

def load_configurations(caminho_config="config/settings.conf"):
    if not errors.exists_path(caminho_config):
        errors.show_simple_error(f"Arquivo de configuração não encontrado: {caminho_config}", "ler_configuracoes")
        return False

    config = ConfigParser()
    config.read(caminho_config, encoding='utf-8')

    conf = config["DEFAULT"]
    return {
        "default_path": conf.get("default_path", "."),
        "default_output": conf.get("default_output", "saida.json"),
        "extensions": [ext.strip() for ext in conf.get("extensions", "").split(",") if ext.strip()],
        "ignore": [pattern.strip() for pattern in conf.get("ignore", "").split(",") if pattern.strip()]
    }
