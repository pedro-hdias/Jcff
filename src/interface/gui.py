import sys

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt
from accessible_output2.outputs.auto import Auto

from utils.logger import registrar

auto = Auto()

def speech(t):
	auto.speak(t)

def exibir_interface():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Gerador de JSON de Estrutura")

    layout = QVBoxLayout()

    titulo = QLabel("Menu Principal")
    layout.addWidget(titulo)

    speech("Menu Principal")

    def acao(msg):
        QMessageBox.information(window, "Ação executada", msg)

    def adicionar_botao(texto, mensagem_log, mensagem_exibida):
        botao = QPushButton(texto)
        botao.setFixedHeight(35)
        botao.setFocusPolicy(Qt.StrongFocus)
        botao.setAutoDefault(True)
        botao.clicked.connect(lambda: [registrar(mensagem_log, nivel="info", local="gui"), acao(mensagem_exibida)])
        layout.addWidget(botao)
        return botao

    botoes = [
        adicionar_botao("1 - Executar com configuração salva", "Opção 1 selecionada na GUI", "Executando com configuração salva"),
        adicionar_botao("2 - Executar com valores personalizados", "Opção 2 selecionada na GUI", "Executando com valores personalizados"),
        adicionar_botao("3 - Ver configuração salva", "Opção 3 selecionada na GUI", "Exibindo configuração salva"),
        adicionar_botao("4 - Configurar", "Opção 4 selecionada na GUI", "Abrindo configuração"),
        adicionar_botao("5 - Sair", "Saída da interface gráfica (PySide6)", "Saindo do programa")
    ]

    botoes[-1].clicked.connect(window.close)
    botoes[0].setFocus()

    window.setLayout(layout)
    registrar("Interface gráfica (PySide6) iniciada", nivel="info", local="gui")
    window.show()
    app.exec()
