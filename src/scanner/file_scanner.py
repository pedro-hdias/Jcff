import os

EXTENSOES_SUPORTADAS = ['.epub', '.txt', '.pdf']

def scan_directory(path, ignore_list=None, base_dir=None):
    if ignore_list is None:
        ignore_list = []

    if base_dir is None:
        base_dir = path

    estrutura = {}

    try:
        itens = sorted(os.listdir(path))
    except PermissionError:
        return {}

    for item in itens:
        if item.startswith('.') or item in ignore_list:
            continue

        caminho_completo = os.path.join(path, item)

        if os.path.isdir(caminho_completo):
            subestrutura = scan_directory(caminho_completo, ignore_list, base_dir)
            if subestrutura:
                estrutura.setdefault("categorias", {})[item] = subestrutura
        elif os.path.isfile(caminho_completo):
            _, ext = os.path.splitext(item)
            if ext.lower() in EXTENSOES_SUPORTADAS:
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
