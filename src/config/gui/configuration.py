from PySide6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QFileDialog,
    QHBoxLayout, QVBoxLayout, QFormLayout, QMessageBox, QWidget
)
from PySide6.QtCore import Qt

from config.settings_reader import load_configurations
from config.settings_writer import save_configuration
from utils import errors
from utils.logger import record_activity
from utils.speech import speech

class ConfigurationDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuração do Programa")
        self.setMinimumSize(600, 400)
        self.setAccessibleName("Tela de Configuração")

        self.base_directory_input = None
        self.output_file_input = None
        self.allowed_extensions_input = None
        self.ignored_patterns_input = None

    def show_dialog(self, dialog_title, dialog_message):
        record_activity(
            f"Showing dialogue: {dialog_title} - {dialog_message}", nivel="info", local="ConfigurationDialog"
        )
        configuration_dialog = QMessageBox(self)
        configuration_dialog.setWindowTitle(dialog_title)
        configuration_dialog.setText(dialog_message)
        configuration_dialog.setStandardButtons(QMessageBox.Ok)
        configuration_dialog.setIcon(QMessageBox.Information)
        configuration_dialog.setStyleSheet(
            "background-color: #f0f0f0; color: #333; font-size: 14px;"
        )
        configuration_dialog.exec_()

    def _validate_input_fields(self):
        if not errors.validate_not_empty(self.base_directory_input.text()):
            errors.show_simple_error(
                "Diretório base não pode ser vazio.", "ConfigurationDialog"
            )
            return False

        if not errors.exists_path(self.base_directory_input.text()):
            errors.show_simple_error("Diretório base não existe.", "ConfigurationDialog")
            return False

        if not errors.validate_directory(self.base_directory_input.text()):
            errors.show_simple_error("Diretório base inválido.", "ConfigurationDialog")
            return False

        if not errors.validate_access(self.base_directory_input.text()):
            errors.show_simple_error(
                "Acesso ao diretório base negado.", "ConfigurationDialog"
            )
            return False

        if not errors.validate_not_empty(self.output_file_input.text()):
            errors.show_simple_error(
                "Arquivo de saída não pode ser vazio.", "ConfigurationDialog"
            )
            return False

        return True
    
    def _save_settings(self):
        speech("Salvando configurações.")
        record_activity("Saving settings", nivel="info", local="ConfigurationDialog")

        if not self._validate_input_fields():
            errors.show_simple_error("Erro ao validar os inputs.", "ConfigurationDialog")
            return

        record_activity(
            "Successful validated inputs", nivel="info", local="ConfigurationDialog"
        )

        settings_dict = {
            "default_path": self.base_directory_input.text(),
            "default_output": self.output_file_input.text(),
            "extensions": [ext.strip() for ext in self.allowed_extensions_input.text().split(",")],
            "ignore": [p.strip() for p in self.ignored_patterns_input.text().split(",")]
        }
        record_activity(
            "Successful Settings Success", nivel="info", local="ConfigurationDialog"
        )
        record_activity(
            f"Configurações: {settings_dict}", nivel="debug", local="ConfigurationDialog"
        )
        try:
             save_configuration(settings_dict)
        except Exception as e:
            errors.show_simple_error(
                f"Erro ao salvar configurações: {e}", "ConfigurationDialog"
            )
            return

        speech("Configurações salvas com sucesso.")
        record_activity(
            "saved settings with success", nivel="info", local="ConfigurationDialog"
        )
        self.show_dialog("Sucesso", "Configurações salvas com sucesso.")
        self.close()

    def execute(self):
        speech("Iniciando configuração do programa.")
        record_activity(
            "Starting Program Configuration", nivel="info", local="ConfigurationDialog"
        )

        configuration_layout = QVBoxLayout()
        form_layout_fields = QFormLayout()

        self.base_directory_input = QLineEdit()
        self.base_directory_input.setAccessibleName("Diretório base")
        self.base_directory_input.setToolTip(
            "Insira o diretório base onde os arquivos deverão ser indexados."
        )

        select_base_directory_button = QPushButton("📁")
        select_base_directory_button.setAccessibleName("Diretório")
        select_base_directory_button.setToolTip(
            "Clique para selecionar o diretório base."
        )
        select_base_directory_button.clicked.connect(lambda: 
            self.base_directory_input.setText(
                QFileDialog.getExistingDirectory(
                    self, "Selecione o diretório base"
                )
            )
        )

        help_button_base_directory = QPushButton("❓")
        help_button_base_directory.setAccessibleName("Ajuda")
        help_button_base_directory.setToolTip(
            "Clique para abrir a ajuda sobre o diretório base."
        )
        help_button_base_directory.clicked.connect(lambda: 
            self.show_dialog(
                "Ajuda", "Selecione o diretório base onde os arquivos deverão ser indexados."
            )
        )

        base_directory_layout = QHBoxLayout()
        base_directory_layout.addWidget(self.base_directory_input)
        base_directory_layout.addWidget(select_base_directory_button)
        base_directory_layout.addWidget(help_button_base_directory)
        form_layout_fields.addRow("Diretório base:", base_directory_layout)

        self.output_file_input = QLineEdit()
        self.output_file_input.setAccessibleName("Arquivo de saída")
        self.output_file_input.setToolTip("Insira o caminho do arquivo de saída padrão.")
        self.output_file_input.setPlaceholderText("Ex: /caminho/para/arquivo.json")

        btn_select_output_file = QPushButton("📄")
        btn_select_output_file.setAccessibleName("Arquivo de saída")
        btn_select_output_file.setToolTip(
            "Clique para selecionar o arquivo de saída padrão."
        )
        btn_select_output_file.clicked.connect(lambda: 
            self.output_file_input.setText(
                QFileDialog.getSaveFileName(
                    self, "Salvar arquivo de saída", "", "JSON Files (*.json)"
                )[0]
            )
        )

        btn_help_output_file = QPushButton("❓")
        btn_help_output_file.setAccessibleName("Ajuda")
        btn_help_output_file.setToolTip(
            "Clique para abrir a ajuda sobre o arquivo de saída."
        )
        btn_help_output_file.clicked.connect(lambda: 
            QMessageBox.information(
                self, "Ajuda", "Selecione o arquivo de saída onde o JSON será salvo."
            )
        )

        output_file_layout = QHBoxLayout()
        output_file_layout.addWidget(self.output_file_input)
        output_file_layout.addWidget(btn_select_output_file)
        output_file_layout.addWidget(btn_help_output_file)
        form_layout_fields.addRow("Arquivo de saída:", output_file_layout)

        self.allowed_extensions_input = QLineEdit()
        self.allowed_extensions_input.setAccessibleName("Extensões permitidas:")
        self.allowed_extensions_input.setToolTip(
            "Insira as extensões permitidas, separadas por vírgula."
        )
        self.allowed_extensions_input.setPlaceholderText("Ex: .php,.html,.css")

        btn_help_allowed_extensions = QPushButton("❓")
        btn_help_allowed_extensions.setAccessibleName("Ajuda")
        btn_help_allowed_extensions.setToolTip(
            "Clique para abrir a ajuda sobre as extensões permitidas."
        )
        btn_help_allowed_extensions.clicked.connect(lambda: 
            QMessageBox.information(
                self, "Ajuda", "Selecione o arquivo de texto contendo as extensões permitidas."
            )
        )

        allowed_extensions_layout = QHBoxLayout()
        allowed_extensions_layout.addWidget(self.allowed_extensions_input)
        allowed_extensions_layout.addWidget(btn_help_allowed_extensions)
        form_layout_fields.addRow("Extensões permitidas:", allowed_extensions_layout)

        self.ignored_patterns_input = QLineEdit()
        self.ignored_patterns_input.setAccessibleName("Padrões a serem ignorados")
        self.ignored_patterns_input.setToolTip(
            "Insira os padrões a serem ignorados, separados por vírgula."
        )
        self.ignored_patterns_input.setPlaceholderText("Ex: .git,.svn")

        btn_help_ignored_patterns = QPushButton("❓")
        btn_help_ignored_patterns.setAccessibleName("Ajuda")
        btn_help_ignored_patterns.setToolTip(
            "Clique para abrir a ajuda sobre os padrões a serem ignorados."
        )
        btn_help_ignored_patterns.clicked.connect(lambda: 
            QMessageBox.information(
                self, "Ajuda", "Insira os padrões a serem ignorados, separados por vírgula. Por exemplo: .php,.html,.css"
            )
        )

        ignored_patterns_layout = QHBoxLayout()
        ignored_patterns_layout.addWidget(self.ignored_patterns_input)
        ignored_patterns_layout.addWidget(btn_help_ignored_patterns)
        form_layout_fields.addRow("Ignorar padrões:", ignored_patterns_layout)

        btn_save = QPushButton("📎")
        btn_save.setAccessibleName("Salvar")
        btn_save.setToolTip("Clique para salvar as configurações.")
        btn_save.clicked.connect(self._save_settings)
        btn_save.clicked.connect(lambda: self._save_settings(self))

        btn_cancel = QPushButton("❌")
        btn_cancel.setAccessibleName("Cancelar")
        btn_cancel.setToolTip("Clique para cancelar.")
        btn_cancel.clicked.connect(lambda: 
            (
                record_activity(
                    "Execução personalizada cancelada", nivel="info", local="ConfigurationDialog"
                ), 
                self.close()
            )
        )

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(btn_save)
        button_layout.addWidget(btn_cancel)

        configuration_layout.addLayout(form_layout_fields)
        configuration_layout.addLayout(button_layout)

        self.setLayout(configuration_layout)
        QWidget.show(self)