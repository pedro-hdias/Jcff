import sys

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt

from config.gui.configuration import TelaConfiguracao
from interface.actions import preset_configuration, custon_execution
from utils.logger import registrar
from utils.speech import speech

app = QApplication(sys.argv)
window = QWidget()
layout_vertical = QVBoxLayout()
tela_configuracao = TelaConfiguracao()      

def acao(executar):
    match executar:
        case "1":
            try:
                preset_configuration.executar_com_configuracao_salva() 
            except Exception as e:
                registrar(f"Erro ao executar com configuração salva: {e}", nivel="error", local="gui")
        case "2":
            try:
                custon_execution.ExecucaoCustomizada().executar()
            except Exception as e:
                registrar(f"Erro ao executar com valores personalizados: {e}", nivel="error", local="gui")
        case "3":
            exibir_configuracao_salva()
        case "4":
            iniciar_configuracao()
        case "5":
            speech("Encerrando...\n")


def criar_botao(texto, mensagem_log, executar):
    botao = QPushButton(texto)
    botao.setFixedHeight(35)
    botao.setFocusPolicy(Qt.StrongFocus)
    botao.setAutoDefault(True)
    botao.clicked.connect(lambda: 
    [registrar(mensagem_log, nivel="info", local="gui"), acao(executar)])
    botao.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px; border-radius: 5px;")
    return botao

def exibir_interface():
    window.setWindowTitle("Gerador de JSON de Estrutura")

    ben_vindo()

    titulo = QLabel("Menu Principal")
    layout_horizontal = QHBoxLayout()
    layout_horizontal.addWidget(titulo)
    speech("Menu Principal")

    botao1 = criar_botao("Executar com configuração salva", "Opção 1 selecionada", "1")
    botao2 = criar_botao("Executar com valores personalizados", "Opção 2 selecionada", "2")
    botao3 = criar_botao("Ver configuração salva", "Opção 3 selecionada", "3")
    botao4 = criar_botao("Configurar", "Opção 4 selecionada", "4")
    botao5 = criar_botao("Sair", "Opção 5 selecionada", "5")

    botao5.clicked.connect(window.close)

    linha1 = QHBoxLayout()
    linha1.addWidget(botao1)
    linha1.addWidget(botao2)

    linha2 = QHBoxLayout()
    linha2.addWidget(botao3)
    linha2.addWidget(botao4)

    layout_vertical.addLayout(linha1)
    layout_vertical.addLayout(linha2)
    layout_vertical.addWidget(botao5)

    window.setLayout(layout_vertical)
    registrar("Interface gráfica (PySide6) iniciada", nivel="info", local="gui")
    window.show()
    app.exec()

def ben_vindo():
    speech("Bem-vindo ao Gerador de JSON de Estrutura")
    msg = QMessageBox()
    registrar("Mensagem de boas-vindas exibida", nivel="info", local="gui")