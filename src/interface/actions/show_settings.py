from PySide6.QtWidgets import (
    QDialog, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QFormLayout
)
from PySide6.QtCore import Qt

from config.settings_reader import load_configurations
from config.gui.configuration import ConfigurationDialog
from utils import errors
from utils.logger import record_activity
from utils.speech import speech

class ConfigurationDisplay(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuração Salva")
        self.setMinimumSize(600, 400)

    def _display_edit_settings(self):
        record_activity(
            "Opening Settings Editing Screen", nivel="info", local="ConfigurationDisplay"
        )
        settings_screen = ConfigurationDialog()
        settings_screen.execute()
        self.close()

    def execute(self):
        speech("Exibindo configuração atual")
        record_activity(
            "Displaying current configuration", nivel="info", local="ConfigurationDisplay"
        )

        loaded_settings = load_configurations()

        record_activity(
            "loaded configuration", nivel="info", local="ConfigurationDisplay"
        )
        record_activity(loaded_settings, nivel="debug", local="ConfigurationDisplay")

        main_layout = QVBoxLayout()
        form_layout_fields = QFormLayout()

        self.input_base_directory = QLineEdit(loaded_settings.get("default_path", ""))
        self.input_base_directory.setReadOnly(True)
        self.input_base_directory.setToolTip("Diretório base")
        self.input_base_directory.setAccessibleName("Diretório base")

        form_layout_fields.addRow("Diretório base:", self.input_base_directory)

        self.output_file_path = QLineEdit(loaded_settings.get("default_output", ""))
        self.output_file_path.setReadOnly(True)
        self.output_file_path.setToolTip("Arquivo de saída")
        self.output_file_path.setAccessibleName("Arquivo de saída")

        form_layout_fields.addRow("Arquivo de saída:", self.output_file_path)

        self.input_allowed_extensions = QLineEdit(
            ", ".join(
                loaded_settings.get(
                    "extensions", []
                )
            )
        )
        self.input_allowed_extensions.setToolTip("Extensões permitidas")
        self.input_allowed_extensions.setAccessibleName("Extensões permitidas")
        self.input_allowed_extensions.setReadOnly(True)

        form_layout_fields.addRow("Extensões permitidas:", self.input_allowed_extensions)

        self.input_ignore_patterns = QLineEdit(
            ", ".join(
                loaded_settings.get(
                    "ignore", []
                )
            )
        )
        self.input_ignore_patterns.setToolTip("Padrões a serem ignorados")
        self.input_ignore_patterns.setAccessibleName("Padrões a serem ignorados")
        self.input_ignore_patterns.setReadOnly(True)

        form_layout_fields.addRow("Ignorar padrões:", self.input_ignore_patterns)

        btn_edit_configuration = QPushButton("✏️")
        btn_edit_configuration.setToolTip("Editar configurações")
        btn_edit_configuration.setAccessibleName("Editar configurações")

        btn_close = QPushButton("❌")
        btn_close.setToolTip("Fechar")
        btn_close.setAccessibleName("Fechar")

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(btn_edit_configuration)
        button_layout.addWidget(btn_close)

        main_layout.addLayout(form_layout_fields)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        btn_edit_configuration.clicked.connect(lambda: self._display_edit_settings())
        btn_close.clicked.connect(lambda: self.close())

        self.setLayout(main_layout)
        self.show()
        record_activity("Showing Screen", nivel="info", local="ConfigurationDisplay")