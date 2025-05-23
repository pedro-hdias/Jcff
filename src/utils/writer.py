import os
import json

def write_json(path, data, ensure_folder=True):
    """
    Escreve um dicionário em formato JSON no caminho especificado.
    Cria a pasta automaticamente se 'ensure_folder' for True.
    """
    try:
        if ensure_folder:
            os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True

    except Exception as e:
        print(f"[WRITER] Falha ao escrever o arquivo: {str(e)}")
        return False
