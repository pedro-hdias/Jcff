from PySide6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QFormLayout, QMessageBox
)
from PySide6.QtCore import Qt
from config.settings_reader import ler_configuracoes
from config.gui.configuration import TelaConfiguracao

class ExibirConfiguracao(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuração Salva (Somente Leitura)")
        self.setMinimumSize(600, 400)

    def abrir_edicao(self):
        tela = TelaConfiguracao()
        # aguardar a edição e atualizar a tela
        tela.executar()
        self.close()
        self.executar()

    def executar(self):
        config = ler_configuracoes()
        layout_geral = QVBoxLayout()
        layout_campos = QFormLayout()

        self.input_diretorio = QLineEdit(config.get("default_path", ""))
        self.input_diretorio.setReadOnly(True)
        self.input_diretorio.setToolTip("Diretório base")
        self.input_diretorio.setAccessibleName("Diretório base")

        layout_campos.addRow("Diretório base:", self.input_diretorio)

        self.input_saida = QLineEdit(config.get("default_output", ""))
        self.input_saida.setReadOnly(True)
        self.input_saida.setToolTip("Arquivo de saída")
        self.input_saida.setAccessibleName("Arquivo de saída")

        layout_campos.addRow("Arquivo de saída:", self.input_saida)

        self.input_extensoes = QLineEdit(", ".join(config.get("extensions", [])))
        self.input_extensoes.setToolTip("Extensões permitidas")
        self.input_extensoes.setAccessibleName("Extensões permitidas")
        self.input_extensoes.setReadOnly(True)

        layout_campos.addRow("Extensões permitidas:", self.input_extensoes)

        self.input_ignorar = QLineEdit(", ".join(config.get("ignore", [])))
        self.input_ignorar.setToolTip("Padrões a serem ignorados")
        self.input_ignorar.setAccessibleName("Padrões a serem ignorados")
        self.input_ignorar.setReadOnly(True)

        layout_campos.addRow("Ignorar padrões:", self.input_ignorar)

        btn_editar = QPushButton("✏️")
        btn_editar.setToolTip("Editar configurações")
        btn_editar.setAccessibleName("Editar configurações")

        btn_fechar = QPushButton("❌")
        btn_fechar.setToolTip("Fechar")
        btn_fechar.setAccessibleName("Fechar")

        linha_botoes = QHBoxLayout()
        linha_botoes.setAlignment(Qt.AlignCenter)
        linha_botoes.addWidget(btn_editar)
        linha_botoes.addWidget(btn_fechar)

        layout_geral.addLayout(layout_campos)
        layout_geral.addLayout(linha_botoes)
        self.setLayout(layout_geral)

        btn_editar.clicked.connect(self.abrir_edicao)
        btn_fechar.clicked.connect(self.close)

        self.setLayout(layout_geral)
        self.show()