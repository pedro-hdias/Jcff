from cli.controller import initialize_context
from utils.logger import record_activity

def main():
    record_activity("Beginning of execution", nivel="info", local="main")
    while True:
        if not initialize_context():
            break
    record_activity("Successful execution", nivel="info", local="main")

if __name__ == "__main__":
    main()
