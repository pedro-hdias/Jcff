import fnmatch

def is_valid_file(filename, allowed_extensions):
    """
    Aceita todos os arquivos se allowed_extensions for None ou vazio.
    Caso contrário, aplica o filtro de extensão.
    """
    if not allowed_extensions:
        return True
    return any(filename.lower().endswith(ext.lower()) for ext in allowed_extensions)

def should_ignore(name, ignore_list):
    """
    Não ignora nada se ignore_list for None ou vazio.
    Caso contrário, verifica padrões com suporte a curingas (*).
    """
    if not ignore_list:
        return False
    return any(fnmatch.fnmatch(name.lower(), pattern.lower()) for pattern in ignore_list)
