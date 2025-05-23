# Módulo responsável por armazenar e fornecer o contexto de execução
# (CLI ou GUI) para que outros módulos possam se adaptar ao ambiente.

_context = "cli"  # valor padrão seguro

def set_context(modo):
    global _context
    if modo in ("cli", "gui"):
        _context = modo
    else:
        raise ValueError("Modo de contexto inválido. Use 'cli' ou 'gui'.")

def get_context():
    return _context

def is_cli():
    return _context == "cli"

def is_gui():
    return _context == "gui"
