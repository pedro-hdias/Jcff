import os
from configparser import ConfigParser
from .settings_writer import salvar_configuracoes

def iniciar_configuracao():
    print("🔧 Iniciando configuração interativa do projeto...\n")

    path = input("1. Caminho padrão para escanear (ex: ./biblioteca): ").strip() or "./biblioteca"
    output = input("2. Nome do arquivo de saída (ex: estrutura.json): ").strip() or "estrutura.json"
    
    extensoes = input("3. Extensões permitidas separadas por vírgula (ex: .pdf,.epub,.txt) [Enter para nenhuma]: ").strip()
    if extensoes:
        extensoes = [ext.strip() for ext in extensoes.split(",")]
    else:
        extensoes = []

    ignorar = input("4. Padrões a ignorar separados por vírgula (ex: *.log,temp*,__pycache__) [Enter para nenhum]: ").strip()
    if ignorar:
        ignorar = [p.strip() for p in ignorar.split(",")]
    else:
        ignorar = []

    configuracoes = {
        "default_path": path,
        "default_output": output,
        "extensions": extensoes,
        "ignore": ignorar
    }

    salvar_configuracoes(configuracoes)
    print("\n✅ Arquivo de configuração criado com sucesso!")

if __name__ == "__main__":
    iniciar_configuracao()
