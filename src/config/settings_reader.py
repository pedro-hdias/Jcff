import os
from configparser import ConfigParser

def ler_configuracoes(caminho_config="config/settings.conf"):
    if not os.path.exists(caminho_config):
        return {}

    config = ConfigParser()
    config.read(caminho_config, encoding='utf-8')

    conf = config["DEFAULT"]
    return {
        "default_path": conf.get("default_path", "."),
        "default_output": conf.get("default_output", "saida.json"),
        "extensions": [ext.strip() for ext in conf.get("extensions", "").split(",") if ext.strip()],
        "ignore": [pattern.strip() for pattern in conf.get("ignore", "").split(",") if pattern.strip()]
    }
