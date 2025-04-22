from PySide6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QFileDialog,
    QHBoxLayout, QVBoxLayout, QFormLayout, QMessageBox, QWidget
)

class TelaConfiguracao(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuração do Programa")
        self.setMinimumSize(600, 400)

        layout_geral = QVBoxLayout()
        layout_campos = QFormLayout()

        # === Diretório Base ===
        self.input_diretorio = QLineEdit()
        btn_pasta = QPushButton("📁")
        btn_ajuda_pasta = QPushButton("❓")

        linha_diretorio = QHBoxLayout()
        linha_diretorio.addWidget(self.input_diretorio)
        linha_diretorio.addWidget(btn_pasta)
        linha_diretorio.addWidget(btn_ajuda_pasta)
        layout_campos.addRow("Diretório base:", linha_diretorio)

        # === Arquivo de saída ===
        self.input_saida = QLineEdit()
        btn_arquivo = QPushButton("📄")
        btn_ajuda_saida = QPushButton("❓")

        linha_saida = QHBoxLayout()
        linha_saida.addWidget(self.input_saida)
        linha_saida.addWidget(btn_arquivo)
        linha_saida.addWidget(btn_ajuda_saida)
        layout_campos.addRow("Arquivo de saída:", linha_saida)

        # === Extensões permitidas ===
        self.input_extensoes = QLineEdit()
        btn_extensoes = QPushButton("📜")
        btn_ajuda_extensoes = QPushButton("❓")

        linha_extensoes = QHBoxLayout()
        linha_extensoes.addWidget(self.input_extensoes)
        linha_extensoes.addWidget(btn_extensoes)
        linha_extensoes.addWidget(btn_ajuda_extensoes)
        layout_campos.addRow("Extensões permitidas:", linha_extensoes)

        # === Padrões a ignorar ===
        self.input_ignorar = QLineEdit()
        btn_ajuda_ignorar = QPushButton("❓")

        linha_ignorar = QHBoxLayout()
        linha_ignorar.addWidget(self.input_ignorar)
        linha_ignorar.addWidget(btn_ajuda_ignorar)
        layout_campos.addRow("Ignorar padrões:", linha_ignorar)

        # === Botões finais (Salvar e Cancelar) ===
        btn_salvar = QPushButton("💾 Salvar")
        btn_cancelar = QPushButton("❌ Cancelar")
        linha_botoes = QHBoxLayout()
        linha_botoes.setAlignment(Qt.AlignCenter)
        linha_botoes.addWidget(btn_salvar)
        linha_botoes.addWidget(btn_cancelar)

        # === Montagem final ===
        layout_geral.addLayout(layout_campos)
        layout_geral.addLayout(linha_botoes)

        self.setLayout(layout_geral)
