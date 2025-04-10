import fnmatch

def is_valid_file(filename, allowed_extensions):
    """
    Verifica se o arquivo tem uma das extensões permitidas.
    """
    return any(filename.lower().endswith(ext.lower()) for ext in allowed_extensions)

def should_ignore(name, ignore_list):
    """
    Verifica se o nome do arquivo ou pasta deve ser ignorado com base em padrões.
    Suporta curingas como *.log ou temp*
    """
    for pattern in ignore_list:
        if fnmatch.fnmatch(name.lower(), pattern.lower()):
            return True
    return False
