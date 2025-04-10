import os
from .filters import is_valid_file, should_ignore

def scan_directory(path, ignore_list=None, allowed_extensions=None, base_dir=None):
    if base_dir is None:
        base_dir = path

    estrutura = {}

    try:
        itens = sorted(os.listdir(path))
    except PermissionError:
        return {}

    for item in itens:
        if item.startswith('.') or should_ignore(item, ignore_list):
            continue

        caminho_completo = os.path.join(path, item)

        if os.path.isdir(caminho_completo):
            subestrutura = scan_directory(
                caminho_completo,
                ignore_list=ignore_list,
                allowed_extensions=allowed_extensions,
                base_dir=base_dir
            )
            if subestrutura:
                estrutura.setdefault("categorias", {})[item] = subestrutura

        elif os.path.isfile(caminho_completo):
            if is_valid_file(item, allowed_extensions):
                caminho_relativo = os.path.relpath(caminho_completo, base_dir)
                if "arquivos" not in estrutura:
                    estrutura["arquivos"] = []
                estrutura["arquivos"].append({
                    "nome_arquivo": item,
                    "caminho": caminho_relativo.replace("\\", "/")
                })

    if "arquivos" in estrutura:
        estrutura["qtd_arquivos"] = len(estrutura["arquivos"])

    return estrutura
