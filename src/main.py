import argparse
import os
from scanner.file_scanner import scan_directory
from exporter.json_formatter import format_json
import json

def main():
    parser = argparse.ArgumentParser(description='Gera um JSON com a estrutura de arquivos.')
    parser.add_argument('--path', type=str, default='.', help='Caminho da pasta base a ser escaneada.')
    parser.add_argument('--output', type=str, default='saida.json', help='Nome do arquivo de saída JSON.')

    args = parser.parse_args()
    base_path = os.path.abspath(args.path)

    if not os.path.isdir(base_path):
        print(f"[Erro] O caminho '{base_path}' não é um diretório válido.")
        return

    print(f"[INFO] Escaneando a pasta: {base_path}")

    estrutura = {
        "secoes": scan_directory(base_path)
    }

    resultado = format_json(estrutura)

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print(f"[OK] JSON gerado em: {args.output}")

if __name__ == "__main__":
    main()
