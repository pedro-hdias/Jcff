import sys

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt

from config.gui.configuration import TelaConfiguracao
from interface.actions import preset_configuration, custon_execution, show_settings
from utils.logger import record_activity
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
                record_activity(f"Erro ao executar com configuração salva: {e}", nivel="error", local="gui")
        case "2":
            try:
                custon_execution.ExecucaoCustomizada().executar()
            except Exception as e:
                record_activity(f"Erro ao executar com valores personalizados: {e}", nivel="error", local="gui")
        case "3":
            try:
                show_settings.ExibirConfiguracao().executar()
            except Exception as e:
                record_activity(f"Erro ao exibir configuração salva: {e}", nivel="error", local="gui")
        case "4":
            try:
                tela_configuracao.executar()
            except Exception as e:
                record_activity(f"Erro ao abrir tela de configuração: {e}", nivel="error", local="gui")
        case "5":
            speech("Encerrando...\n")
            record_activity("Encerrando o programa", nivel="info", local="gui")
            sys.exit(0)

def criar_botao(texto, mensagem_log, executar):
    botao = QPushButton(texto)
    botao.setFixedHeight(35)
    botao.setFocusPolicy(Qt.StrongFocus)
    botao.setAutoDefault(True)
    botao.clicked.connect(lambda: 
    [record_activity(mensagem_log, nivel="info", local="gui"), acao(executar)])
    botao.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px; border-radius: 5px;")
    return botao

def show_gui_interface():
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
    record_activity("Interface gráfica (PySide6) iniciada", nivel="info", local="gui")
    window.show()
    app.exec()

def ben_vindo():
    speech("Bem-vindo ao Gerador de JSON de Estrutura")
    msg = QMessageBox()
    record_activity("Mensagem de boas-vindas exibida", nivel="info", local="gui")