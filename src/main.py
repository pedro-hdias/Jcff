from cli.controller import continuar

def main():
    while True:
        if not continuar():
            break

if __name__ == "__main__":
    main()
