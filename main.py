import sys

from PySide6.QtWidgets import QApplication

from interface import Interface

from banco import criar_tabela


if __name__ == "__main__":
    criar_tabela()

    app = QApplication(sys.argv)

    janela = Interface()
    janela.showMaximized()

    sys.exit(app.exec())