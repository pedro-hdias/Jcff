from cli.controller import initialize_context
from utils.logger import record_activity

def main():
    record_activity("Beginning of execution", log_level="info", log_origin="main")
    while True:
        if not initialize_context():
            break
    record_activity("Successful execution", log_level="info", log_origin="main")

if __name__ == "__main__":
    main()
