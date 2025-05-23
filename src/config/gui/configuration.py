from PySide6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QFileDialog,
    QHBoxLayout, QVBoxLayout, QFormLayout, QMessageBox, QWidget
)
from PySide6.QtCore import Qt

from config.settings_reader import ler_configuracoes
from config.settings_writer import salvar_configuracoes
from utils import errors
from utils.logger import registrar
from utils.speech import speech

class TelaConfiguracao(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuração do Programa")
        self.setMinimumSize(600, 400)
        self.setAccessibleName("Tela de Configuração")

        self.input_diretorio = None
        self.input_saida = None
        self.input_extensoes = None
        self.input_ignorar = None

    def dialogs(self, titulo, mensagem):
        registrar(f"Exibindo diálogo: {titulo} - {mensagem}", nivel="info", local="TelaConfiguracao")
        dialogo = QMessageBox(self)
        dialogo.setWindowTitle(titulo)
        dialogo.setText(mensagem)
        dialogo.setStandardButtons(QMessageBox.Ok)
        dialogo.setIcon(QMessageBox.Information)
        dialogo.setStyleSheet("background-color: #f0f0f0; color: #333; font-size: 14px;")
        dialogo.exec_()

    def _validar_inputs(self):
        if not errors.validate_not_empty(self.input_diretorio.text()):
            errors.show_simple_error("Diretório base não pode ser vazio.", "TelaConfiguracao")
            return False

        if not errors.exists_path(self.input_diretorio.text()):
            errors.show_simple_error("Diretório base não existe.", "TelaConfiguracao")
            return False

        if not errors.validate_directory(self.input_diretorio.text()):
            errors.show_simple_error("Diretório base inválido.", "TelaConfiguracao")
            return False

        if not errors.validate_access(self.input_diretorio.text()):
            errors.show_simple_error("Acesso ao diretório base negado.", "TelaConfiguracao")
            return False

        if not errors.validate_not_empty(self.input_saida.text()):
            errors.show_simple_error("Arquivo de saída não pode ser vazio.", "TelaConfiguracao")
            return False

        return True
    
    def _salvar_configuracoes(self):
        speech("Salvando configurações.")
        registrar("Salvando configurações", nivel="info", local="TelaConfiguracao")

        if not self._validar_inputs():
            errors.show_simple_error("Erro ao validar os inputs.", "TelaConfiguracao")
            return

        registrar("Inputs validados com sucesso", nivel="info", local="TelaConfiguracao")

        configuracoes = {
            "default_path": self.input_diretorio.text(),
            "default_output": self.input_saida.text(),
            "extensions": [ext.strip() for ext in self.input_extensoes.text().split(",")],
            "ignore": [p.strip() for p in self.input_ignorar.text().split(",")]
        }
        registrar("Configurações coletadas com sucesso", nivel="info", local="TelaConfiguracao")
        registrar(f"Configurações: {configuracoes}", nivel="debug", local="TelaConfiguracao")
        try:
             salvar_configuracoes(configuracoes)
        except Exception as e:
            errors.show_simple_error(f"Erro ao salvar configurações: {e}", "TelaConfiguracao")
            return

        speech("Configurações salvas com sucesso.")
        registrar("Configurações salvas com sucesso", nivel="info", local="TelaConfiguracao")
        self.dialogs("Sucesso", "Configurações salvas com sucesso.")
        self.close()

    def executar(self):
        speech("Iniciando configuração do programa.")
        registrar("Iniciando configuração do programa", nivel="info", local="TelaConfiguracao")

        layout_geral = QVBoxLayout()
        layout_campos = QFormLayout()

        self.input_diretorio = QLineEdit()
        self.input_diretorio.setAccessibleName("Diretório base")
        self.input_diretorio.setToolTip("Insira o diretório base onde os arquivos deverão ser indexados.")

        btn_pasta = QPushButton("📁")
        btn_pasta.setAccessibleName("Diretório")
        btn_pasta.setToolTip("Clique para selecionar o diretório base.")
        btn_pasta.clicked.connect(lambda: 
        self.input_diretorio.setText(QFileDialog.getExistingDirectory(self, "Selecione o diretório base")))

        btn_ajuda_pasta = QPushButton("❓")
        btn_ajuda_pasta.setAccessibleName("Ajuda")
        btn_ajuda_pasta.setToolTip("Clique para abrir a ajuda sobre o diretório base.")
        btn_ajuda_pasta.clicked.connect(lambda: self.dialogs("Ajuda", "Selecione o diretório base onde os arquivos deverão ser indexados."))

        linha_diretorio = QHBoxLayout()
        linha_diretorio.addWidget(self.input_diretorio)
        linha_diretorio.addWidget(btn_pasta)
        linha_diretorio.addWidget(btn_ajuda_pasta)
        layout_campos.addRow("Diretório base:", linha_diretorio)

        self.input_saida = QLineEdit()
        self.input_saida.setAccessibleName("Arquivo de saída")
        self.input_saida.setToolTip("Insira o caminho do arquivo de saída padrão.")
        self.input_saida.setPlaceholderText("Ex: /caminho/para/arquivo.json")

        btn_arquivo = QPushButton("📄")
        btn_arquivo.setAccessibleName("Arquivo de saída")
        btn_arquivo.setToolTip("Clique para selecionar o arquivo de saída padrão.")
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

        btn_ajuda_extensoes = QPushButton("❓")
        btn_ajuda_extensoes.setAccessibleName("Ajuda")
        btn_ajuda_extensoes.setToolTip("Clique para abrir a ajuda sobre as extensões permitidas.")
        btn_ajuda_extensoes.clicked.connect(lambda: QMessageBox.information(self, "Ajuda", "Selecione o arquivo de texto contendo as extensões permitidas."))

        linha_extensoes = QHBoxLayout()
        linha_extensoes.addWidget(self.input_extensoes)
        linha_extensoes.addWidget(btn_ajuda_extensoes)
        layout_campos.addRow("Extensões permitidas:", linha_extensoes)

        self.input_ignorar = QLineEdit()
        self.input_ignorar.setAccessibleName("Padrões a serem ignorados")
        self.input_ignorar.setToolTip("Insira os padrões a serem ignorados, separados por vírgula.")
        self.input_ignorar.setPlaceholderText("Ex: .git,.svn")

        btn_ajuda_ignorar = QPushButton("❓")
        btn_ajuda_ignorar.setAccessibleName("Ajuda")
        btn_ajuda_ignorar.setToolTip("Clique para abrir a ajuda sobre os padrões a serem ignorados.")
        btn_ajuda_ignorar.clicked.connect(lambda: QMessageBox.information(self, "Ajuda", "Insira os padrões a serem ignorados, separados por vírgula. Por exemplo: .php,.html,.css"))

        linha_ignorar = QHBoxLayout()
        linha_ignorar.addWidget(self.input_ignorar)
        linha_ignorar.addWidget(btn_ajuda_ignorar)
        layout_campos.addRow("Ignorar padrões:", linha_ignorar)
        btn_salvar = QPushButton("📎")
        btn_salvar.setAccessibleName("Salvar")
        btn_salvar.setToolTip("Clique para salvar as configurações.")
        btn_salvar.clicked.connect(self._salvar_configuracoes)
        btn_salvar.clicked.connect(lambda: self._salvar_configuracoes(self))

        btn_cancelar = QPushButton("❌")
        btn_cancelar.setAccessibleName("Cancelar")
        btn_cancelar.setToolTip("Clique para cancelar.")
        btn_cancelar.clicked.connect(lambda: (registrar("Execução personalizada cancelada", nivel="info", local="TelaConfiguracao"), self.close()))

        linha_botoes = QHBoxLayout()
        linha_botoes.setAlignment(Qt.AlignCenter)
        linha_botoes.addWidget(btn_salvar)
        linha_botoes.addWidget(btn_cancelar)

        layout_geral.addLayout(layout_campos)
        layout_geral.addLayout(linha_botoes)

        self.setLayout(layout_geral)
        QWidget.show(self)