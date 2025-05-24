import sys

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt

from config.gui.configuration import ConfigurationDialog
from interface.actions import preset_configuration, custon_execution, show_settings
from utils.logger import record_activity
from utils.speech import speech

app = QApplication(sys.argv)
window = QWidget()
vertical_layout = QVBoxLayout()
configuration_screen = ConfigurationDialog()      

def execute_action(action_command):
    match action_command:
        case "1":
            try:
                preset_configuration.run_with_preset_config() 
            except Exception as e:
                record_activity(
                    f"Error executing with saved configuration: {e}", log_level="error", log_origin="gui"
                )
        case "2":
            try:
                custon_execution.CustomExecution().execute()
            except Exception as e:
                record_activity(
                    f"Error when executing with personalized values: {e}", log_level="error", log_origin="gui"
                )
        case "3":
            try:
                show_settings.ConfigurationDisplay().execute()
            except Exception as e:
                record_activity(
                    f"Error when displaying save configuration: {e}", log_level="error", log_origin="gui"
                )
        case "4":
            try:
                configuration_screen.execute()
            except Exception as e:
                record_activity(
                    f"Error when opening configuration screen: {e}", log_level="error", log_origin="gui"
                )
        case "5":
            speech("Encerrando...\n")
            record_activity("Closing the Program", log_level="info", log_origin="gui")
            sys.exit(0)

def create_button(button_label, log_message, execute_action):
    button = QPushButton(button_label)
    button.setFixedHeight(35)
    button.setFocusPolicy(Qt.StrongFocus)
    button.setAutoDefault(True)
    button.clicked.connect(lambda: [
        record_activity(log_message, log_level="info", log_origin="gui"),
        execute_action(execute_action)
    ])
    button.setStyleSheet(
        "background-color: #4CAF50; color: white; font-size: 16px; border-radius: 5px;"
    )
    return button

def show_gui_interface():
    window.setWindowTitle("Gerador de JSON de Estrutura")

    show_welcome_message()

    title_label = QLabel("Menu Principal")
    main_menu_layout = QHBoxLayout()
    main_menu_layout.addWidget(title_label)
    speech("Menu Principal")

    button_I = create_button("Executar com configuração salva", "Option 1 selected", "1")
    button_II = create_button(
        "Executar com valores personalizados", "Option 2 selected", "2"
    )
    button_III = create_button("Ver configuração salva", "Option 3 selected", "3")
    button_IV = create_button("Configurar", "Option 4 selected", "4")
    button_V = create_button("Sair", "Option 5 selected", "5")

    button_V.clicked.connect(window.close)

    line_I = QHBoxLayout()
    line_I.addWidget(button_I)
    line_I.addWidget(button_II)

    line_II = QHBoxLayout()
    line_II.addWidget(button_III)
    line_II.addWidget(button_IV)

    vertical_layout.addLayout(line_I)
    vertical_layout.addLayout(line_II)
    vertical_layout.addWidget(button_V)

    window.setLayout(vertical_layout)
    record_activity("Graphic interface(PySide6) initiated", log_level="info", log_origin="gui")
    window.show()
    app.exec()

def show_welcome_message():
    speech("Bem-vindo ao Gerador de JSON de Estrutura")
    msg = QMessageBox()
    record_activity("Welcome message displayed", log_level="info", log_origin="gui")