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
from utils.logger import registrar
from utils.speech import speech

class ExecucaoCustomizada(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Execução personalizada")
        self.setMinimumSize(600, 400)
        self.input_diretorio = None
        self.input_saida = None
        self.input_extensoes = None
        self.input_ignorar = None

    def dialogs(self, titulo, mensagem):
        registrar(f"Exibindo diálogo: {titulo} - {mensagem}", nivel="debug", local="ExecucaoCustomizada")
        dialogo = QMessageBox(self)
        dialogo.setWindowTitle(titulo)
        dialogo.setText(mensagem)
        dialogo.setStandardButtons(QMessageBox.Ok)
        dialogo.setIcon(QMessageBox.Information)
        dialogo.setStyleSheet("background-color: #f0f0f0; color: #333; font-size: 14px;")
        dialogo.exec_()

    def _validar_inputs(self):
        speech("Gerando arquivo JSON com parâmetros personalizados.")
        if not errors.validate_not_empty(self.input_diretorio.text()):
            errors.show_simple_error("Diretório base não pode ser vazio.", "ExecucaoCustomizada")
            return

        if not errors.exists_path(self.input_diretorio.text()):
            errors.show_simple_error("Diretório base não existe.", "ExecucaoCustomizada")
            return

        if not errors.validate_directory(self.input_diretorio.text()):
            errors.show_simple_error("Diretório base inválido.", "ExecucaoCustomizada")
            return

        if not errors.validate_access(self.input_diretorio.text()):
            errors.show_simple_error("Acesso ao diretório base negado.", "ExecucaoCustomizada")
            return

        if not errors.validate_not_empty(self.input_saida.text()):
            errors.show_simple_error("Arquivo de saída não pode ser vazio.", "ExecucaoCustomizada")
            return

    def _gerar_arquivo(self):
        self._validar_inputs()

        path = self.input_diretorio.text().strip()
        output = self.input_saida.text().strip()
        ext = self.input_extensoes.text().strip().split(",")
        ignore = self.input_ignorar.text().strip().split(",")

        ext = [e.strip() for e in ext if e.strip()]
        ignore = [i.strip() for i in ignore if i.strip()]
        path = os.path.abspath(path)

        registrar(f"Personalização - path: {path}, output: {output}, ext: {ext}, ignore: {ignore}", nivel="debug", local="ExecucaoCustomizada")

        estrutura = {
            "secoes": file_scanner.scan_directory(path, ignore, ext)
        }

        with open(output, 'w', encoding='utf-8') as f:
            json.dump(json_formatter.format_json(estrutura), f, ensure_ascii=False, indent=2)

        registrar(f"Arquivo JSON salvo com parâmetros personalizados em: {output}", nivel="info", local="ExecucaoCustomizada")
        self.dialogs(f"Arquivo JSON Gerado", f"Arquivo JSON salvo em: {output}")
        self.close()

    def executar(self):
        speech("Iniciando execução personalizada")
        registrar("Iniciando execução personalizada", nivel="info", local="ExecucaoCustomizada")
        layout_geral = QVBoxLayout()
        layout_campos = QFormLayout()

        self.input_diretorio = QLineEdit()
        self.input_diretorio.setAccessibleName("Diretório base")
        self.input_diretorio.setToolTip("Insira o diretório base onde os arquivos estão localizados.")

        btn_pasta = QPushButton("📁")
        btn_pasta.setAccessibleName("Diretório")
        btn_pasta.setToolTip("Clique para selecionar o diretório base.")
        btn_pasta.clicked.connect(lambda: self.input_diretorio.setText(QFileDialog.getExistingDirectory(self, "Selecione o diretório base")))

        btn_ajuda_pasta = QPushButton("❓")
        btn_ajuda_pasta.setAccessibleName("Ajuda")
        btn_ajuda_pasta.setToolTip("Clique para abrir a ajuda sobre o diretório base.")
        btn_ajuda_pasta.clicked.connect(lambda: self.dialogs("Ajuda", "Selecione o diretório base onde os arquivos estão localizados."))

        linha_diretorio = QHBoxLayout()
        linha_diretorio.addWidget(self.input_diretorio)
        linha_diretorio.addWidget(btn_pasta)
        linha_diretorio.addWidget(btn_ajuda_pasta)
        layout_campos.addRow("Diretório base:", linha_diretorio)

        self.input_saida = QLineEdit()
        self.input_saida.setAccessibleName("Arquivo de saída")
        self.input_saida.setToolTip("Insira o caminho do arquivo de saída.")
        self.input_saida.setPlaceholderText("Ex: /caminho/para/arquivo.json")

        btn_arquivo = QPushButton("📄")
        btn_arquivo.setAccessibleName("Arquivo de saída")
        btn_arquivo.setToolTip("Clique para selecionar o arquivo de saída.")
        btn_arquivo.clicked.connect(lambda: self.input_saida.setText(QFileDialog.getSaveFileName(self, "Salvar arquivo de saída", "", "JSON Files (*.json)")[0]))

        btn_ajuda_saida = QPushButton("❓")
        btn_ajuda_saida.setAccessibleName("Ajuda")
        btn_ajuda_saida.setToolTip("Clique para abrir a ajuda sobre o arquivo de saída.")
        btn_ajuda_saida.clicked.connect(lambda: QMessageBox.information(self, "Ajuda", "Selecione o arquivo de saída onde o JSON será salvo."))

        linha_saida = QHBoxLayout()
        linha_saida.addWidget(self.input_saida)
        linha_saida.addWidget(btn_arquivo)
        linha_saida.addWidget(btn_ajuda_saida)
        layout_campos.addRow("Arquivo de saída:", linha_saida)

        self.input_extensoes = QLineEdit()
        self.input_extensoes.setAccessibleName("Extensões permitidas:")
        self.input_extensoes.setToolTip("Insira as extensões permitidas, separadas por vírgula.")
        self.input_extensoes.setPlaceholderText("Ex: .php,.html,.css")

        btn_extensoes = QPushButton("📜")
        btn_extensoes.setAccessibleName("Extensões permitidas")
        btn_extensoes.setToolTip("Clique para selecionar as extensões permitidas.")
        btn_extensoes.clicked.connect(lambda: self.input_extensoes.setText(QFileDialog.getOpenFileName(self, "Selecionar extensões permitidas", "", "Text Files (*.txt)")[0]))

        btn_ajuda_extensoes = QPushButton("❓")
        btn_ajuda_extensoes.setAccessibleName("Ajuda")
        btn_ajuda_extensoes.setToolTip("Clique para abrir a ajuda sobre as extensões permitidas.")
        btn_ajuda_extensoes.clicked.connect(lambda: QMessageBox.information(self, "Ajuda", "Selecione o arquivo de texto contendo as extensões permitidas."))

        linha_extensoes = QHBoxLayout()
        linha_extensoes.addWidget(self.input_extensoes)
        linha_extensoes.addWidget(btn_extensoes)
        linha_extensoes.addWidget(btn_ajuda_extensoes)
        layout_campos.addRow("Extensões permitidas:", linha_extensoes)

        self.input_ignorar = QLineEdit()
        self.input_ignorar.setAccessibleName("Padrões a serem ignorados")
        self.input_ignorar.setToolTip("Insira os padrões a serem ignorados, separados por vírgula.")
        self.input_ignorar.setPlaceholderText("Ex: *.git, *.log, *.tmp")

        btn_ajuda_ignorar = QPushButton("❓")
        btn_ajuda_ignorar.setAccessibleName("Ajuda")
        btn_ajuda_ignorar.setToolTip("Clique para abrir a ajuda sobre os padrões a serem ignorados.")
        btn_ajuda_ignorar.clicked.connect(lambda: QMessageBox.information(self, "Ajuda", "Insira os padrões a serem ignorados, separados por vírgula. Por exemplo: *.php, *.html, *.css"))

        linha_ignorar = QHBoxLayout()
        linha_ignorar.addWidget(self.input_ignorar)
        linha_ignorar.addWidget(btn_ajuda_ignorar)
        layout_campos.addRow("Ignorar padrões:", linha_ignorar)

        btn_salvar = QPushButton("▶️")
        btn_salvar.setAccessibleName("Executar")
        btn_salvar.setToolTip("Clique para executar a geração do arquivo JSON.")
        btn_salvar.clicked.connect(lambda: self._gerar_arquivo())

        btn_cancelar = QPushButton("❌")
        btn_cancelar.setAccessibleName("Cancelar")
        btn_cancelar.setToolTip("Clique para cancelar a execução.")
        btn_cancelar.clicked.connect(lambda: (registrar("Execução personalizada cancelada", nivel="info", local="ExecucaoCustomizada"), self.close()))

        linha_botoes = QHBoxLayout()
        linha_botoes.setAlignment(Qt.AlignCenter)
        linha_botoes.addWidget(btn_salvar)
        linha_botoes.addWidget(btn_cancelar)

        layout_geral.addLayout(layout_campos)
        layout_geral.addLayout(linha_botoes)

        self.setLayout(layout_geral)
        QWidget.show(self)