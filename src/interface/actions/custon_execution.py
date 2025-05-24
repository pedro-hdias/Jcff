import os
import json

from PySide6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QFileDialog,
    QHBoxLayout, QVBoxLayout, QFormLayout, QMessageBox, QWidget
)
from PySide6.QtCore import Qt

from exporter import json_formatter
from scanner import file_scanner
from utils import errors
from utils.logger import record_activity
from utils.speech import speech

class CustomExecution(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Execução personalizada")
        self.setMinimumSize(600, 400)
        self.base_directory_input = None
        self.output_file_input = None
        self.allowed_extensions_input = None
        self.ignored_patterns_input = None

    def show_dialog(self, dialog_title, dialog_message):
        record_activity(
            f"Showing dialogue: {dialog_title} - {dialog_message}", log_level="debug", log_origin="CustonExecution"
        )
        dialog_window = QMessageBox(self)
        dialog_window.setWindowTitle(dialog_title)
        dialog_window.setText(dialog_message)
        dialog_window.setStandardButtons(QMessageBox.Ok)
        dialog_window.setIcon(QMessageBox.Information)
        dialog_window.setStyleSheet(
            "background-color: #f0f0f0; color: #333; font-size: 14px;"
        )
        dialog_window.exec_()

    def _validate_input_parameters(self):
        speech("Gerando arquivo JSON com parâmetros personalizados.")
        if not errors.validate_not_empty(self.base_directory_input.text()):
            errors.show_simple_error("Diretório base não pode ser vazio.", "CustonExecution")
            return

        if not errors.exists_path(self.base_directory_input.text()):
            errors.show_simple_error("Diretório base não existe.", "CustonExecution")
            return

        if not errors.validate_directory(self.base_directory_input.text()):
            errors.show_simple_error("Diretório base inválido.", "CustonExecution")
            return

        if not errors.validate_access(self.base_directory_input.text()):
            errors.show_simple_error("Acesso ao diretório base negado.", "CustonExecution")
            return

        if not errors.validate_not_empty(self.output_file_input.text()):
            errors.show_simple_error("Arquivo de saída não pode ser vazio.", "CustonExecution")
            return

    def _create_json_file(self):
        self._validate_input_parameters()

        path = self.base_directory_input.text().strip()
        output = self.output_file_input.text().strip()
        ext = self.allowed_extensions_input.text().strip().split(",")
        ignore = self.ignored_patterns_input.text().strip().split(",")

        ext = [e.strip() for e in ext if e.strip()]
        ignore = [i.strip() for i in ignore if i.strip()]
        path = os.path.abspath(path)

        record_activity(
            f"Personalization - path: {path}, output: {output}, ext: {ext}, ignore: {ignore}", log_level="debug", log_origin="CustonExecution")

        json_output = {
            "secoes": file_scanner.scan_directory(path, ignore, ext)
        }

        with open(output, 'w', encoding='utf-8') as f:
            json.dump(json_formatter.format_json(json_output), f, ensure_ascii=False, indent=2)

        record_activity(
            f"JSON File saved with custom parameters in: {output}", log_level="info", log_origin="CustonExecution")
        self.show_dialog(
            f"Arquivo JSON Gerado", f"Arquivo JSON salvo em: {output}"
        )
        self.close()

    def execute(self):
        speech("Iniciando execução personalizada")
        record_activity(
            "Starting Personalized Execution", log_level="info", log_origin="CustonExecution"
        )
        main_layout = QVBoxLayout()
        input_field_layout = QFormLayout()

        self.base_directory_input = QLineEdit()
        self.base_directory_input.setAccessibleName("Diretório base")
        self.base_directory_input.setToolTip(
            "Insira o diretório base onde os arquivos estão localizados."
        )

        btn_select_base_directory = QPushButton("📁")
        btn_select_base_directory.setAccessibleName("Diretório")
        btn_select_base_directory.setToolTip("Clique para selecionar o diretório base.")
        btn_select_base_directory.clicked.connect(lambda: 
            self.base_directory_input.setText(
                QFileDialog.getExistingDirectory(
                    self, "Selecione o diretório base"
                )
            )
        )

        btn_help_directory = QPushButton("❓")
        btn_help_directory.setAccessibleName("Ajuda")
        btn_help_directory.setToolTip(
            "Clique para abrir a ajuda sobre o diretório base."
        )
        btn_help_directory.clicked.connect(lambda: 
            self.show_dialog(
                "Ajuda", "Selecione o diretório base onde os arquivos estão localizados."
            )
        )

        directory_input_row = QHBoxLayout()
        directory_input_row.addWidget(self.base_directory_input)
        directory_input_row.addWidget(btn_select_base_directory)
        directory_input_row.addWidget(btn_help_directory)
        input_field_layout.addRow("Diretório base:", directory_input_row)

        self.output_file_input = QLineEdit()
        self.output_file_input.setAccessibleName("Arquivo de saída")
        self.output_file_input.setToolTip("Insira o caminho do arquivo de saída.")
        self.output_file_input.setPlaceholderText("Ex: /caminho/para/arquivo.json")

        btn_select_output_file = QPushButton("📄")
        btn_select_output_file.setAccessibleName("Arquivo de saída")
        btn_select_output_file.setToolTip("Clique para selecionar o arquivo de saída.")
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

        output_file_row = QHBoxLayout()
        output_file_row.addWidget(self.output_file_input)
        output_file_row.addWidget(btn_select_output_file)
        output_file_row.addWidget(btn_help_output_file)
        input_field_layout.addRow("Arquivo de saída:", output_file_row)

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
                self, "Ajuda", "Escreva as extensões permitidas, separadas por vírgula. EX: .php,.html,.css"
            )
        )

        extensions_input_layout = QHBoxLayout()
        extensions_input_layout.addWidget(self.allowed_extensions_input)
        extensions_input_layout.addWidget(btn_help_allowed_extensions)
        input_field_layout.addRow("Extensões permitidas:", extensions_input_layout)

        self.ignored_patterns_input = QLineEdit()
        self.ignored_patterns_input.setAccessibleName("Padrões a serem ignorados")
        self.ignored_patterns_input.setToolTip(
            "Insira os padrões a serem ignorados, separados por vírgula."
        )
        self.ignored_patterns_input.setPlaceholderText("Ex: *.git, *.log, *.tmp")

        btn_help_ignored_patterns = QPushButton("❓")
        btn_help_ignored_patterns.setAccessibleName("Ajuda")
        btn_help_ignored_patterns.setToolTip(
            "Clique para abrir a ajuda sobre os padrões a serem ignorados."
        )
        btn_help_ignored_patterns.clicked.connect(lambda: 
            QMessageBox.information(
                self, "Ajuda", "Insira os padrões a serem ignorados, separados por vírgula. Por exemplo: *.php, *.html, *.css"
            )
        )

        ignored_patterns_layout = QHBoxLayout()
        ignored_patterns_layout.addWidget(self.ignored_patterns_input)
        ignored_patterns_layout.addWidget(btn_help_ignored_patterns)
        input_field_layout.addRow("Ignorar padrões:", ignored_patterns_layout)

        btn_execute = QPushButton("▶️")
        btn_execute.setAccessibleName("Executar")
        btn_execute.setToolTip("Clique para executar a geração do arquivo JSON.")
        btn_execute.clicked.connect(lambda: self._create_json_file())

        btn_cancel_execution = QPushButton("❌")
        btn_cancel_execution.setAccessibleName("Cancelar")
        btn_cancel_execution.setToolTip("Clique para cancelar a execução.")
        btn_cancel_execution.clicked.connect(lambda: 
            (
                record_activity("Execução personalizada cancelada", log_level="info", log_origin="CustonExecution"),
                self.close()
            )
        )

        action_buttons_layout = QHBoxLayout()
        action_buttons_layout.setAlignment(Qt.AlignCenter)
        action_buttons_layout.addWidget(btn_execute)
        action_buttons_layout.addWidget(btn_cancel_execution)

        main_layout.addLayout(input_field_layout)
        main_layout.addLayout(action_buttons_layout)

        self.setLayout(main_layout)
        QWidget.show(self)