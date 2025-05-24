import os
from scanner.filters import is_valid_file, should_ignore
from utils import errors
from utils.logger import record_activity

def scan_directory(path, ignore_list=None, allowed_extensions=None, base_dir=None):
    record_activity(f"Escaneando diretório: {path}", nivel="info", local="scan_directory")
    record_activity(f"Parâmetros de escaneamento: ignore_list={ignore_list}, allowed_extensions={allowed_extensions}, base_dir={base_dir}", nivel="debug", local="scan_directory")
    if base_dir is None:
        base_dir = path

    estrutura = {}

    try:
        itens = sorted(os.listdir(path))
    except PermissionError:
        errors.show_simple_error(f"Permissão negada para acessar o diretório: {path}")

    for item in itens:
        if item.startswith('.') or should_ignore(item, ignore_list):
            record_activity(f"Ignorando item: {item}", nivel="debug", local="scan_directory")
            continue

        caminho_completo = os.path.join(path, item)
        record_activity(f"Analisando item: {item}", nivel="debug", local="scan_directory")

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

    record_activity(f"Estrutura do diretório '{path}': {estrutura}", nivel="debug", local="scan_directory")
    record_activity(f"Finalizando escaneamento do diretório: {path} com sucesso.", nivel="info", local="scan_directory")
    return estrutura
