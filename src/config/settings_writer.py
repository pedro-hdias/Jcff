import os
from configparser import ConfigParser

def salvar_configuracoes(configuracoes, caminho_config="config/settings.conf"):
    config = ConfigParser()
    config["DEFAULT"] = {
        "default_path": configuracoes.get("default_path", "."),
        "default_output": configuracoes.get("default_output", "saida.json"),
        "extensions": ",".join(configuracoes.get("extensions", [])),
        "ignore": ",".join(configuracoes.get("ignore", []))
    }

    os.makedirs(os.path.dirname(caminho_config), exist_ok=True)

    with open(caminho_config, 'w', encoding='utf-8') as configfile:
        config.write(configfile)
