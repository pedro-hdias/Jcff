import sys
import os
from config.settings_reader import ler_configuracoes
from config.configuration import iniciar_configuracao

# Em breve: importar menu e gui aqui
# from interface.menu import exibir_menu
# from interface.gui import exibir_gui

def foi_executado_com_argumentos():
    return len(sys.argv) > 1

def esta_rodando_como_exe():
    # Quando empacotado em .exe, o atributo sys.frozen é definido
    return getattr(sys, 'frozen', False)

def continuar():
    """
    Esta função é chamada pelo main.py.
    Ela decide o que fazer: rodar direto, chamar menu ou exibir GUI.
    Retorna True para continuar o loop, False para encerrar.
    """
    if foi_executado_com_argumentos():
        print("[Controller] Argumentos detectados. Executando modo CLI direto.\n")
        from main import executar_com_argumentos
        executar_com_argumentos()
        return False

    if esta_rodando_como_exe():
        print("[Controller] Modo .exe detectado. GUI será ativada (ainda em texto).\n")
        # exibir_gui()  ← a gente cria depois
        return False

    print("[Controller] Nenhum argumento. Entrando no menu interativo via terminal.\n")
    # exibir_menu()  ← a gente cria depois
    return False
