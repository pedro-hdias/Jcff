from cli.controller import continuar
from utils.logger import registrar

def main():
    registrar("Início da execução", nivel="info", local="main")
    while True:
        if not continuar():
            break
    registrar("Execução encerrada com sucesso", nivel="info", local="main")

if __name__ == "__main__":
    main()
