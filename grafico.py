from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QPen
import random


class Grafico(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumHeight(120)

        # Pontos do gráfico
        self.valores = []

        # Quantidade de pontos visíveis
        self.quantidade = 45

        # Estado do gráfico
        self.nivel = 0.35

        # Timer da animação
        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.atualizar
        )

        self.timer.start(100)

    # =========================================================
    # ATUALIZAÇÃO
    # =========================================================

    def atualizar(self):

        # Pequena variação natural
        variacao = random.uniform(
            -0.08,
            0.08
        )

        self.nivel += variacao

        # Mantém dentro dos limites
        self.nivel = max(
            0.05,
            min(
                0.95,
                self.nivel
            )
        )

        self.valores.append(
            self.nivel
        )

        # Remove os pontos antigos
        if len(self.valores) > self.quantidade:

            self.valores.pop(0)

        self.update()

    # =========================================================
    # PINTURA
    # =========================================================

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing,
            False
        )

        largura = self.width()
        altura = self.height()

        # =====================================================
        # FUNDO
        # =====================================================

        painter.fillRect(
            0,
            0,
            largura,
            altura,
            Qt.black
        )

        # =====================================================
        # GRADE
        # =====================================================

        grade_pen = QPen(
            Qt.darkGreen
        )

        grade_pen.setWidth(1)

        painter.setPen(
            grade_pen
        )

        # Linhas horizontais
        for i in range(1, 5):

            y = (
                altura * i
            ) // 5

            painter.drawLine(
                0,
                y,
                largura,
                y
            )

        # Linhas verticais
        for i in range(1, 10):

            x = (
                largura * i
            ) // 10

            painter.drawLine(
                x,
                0,
                x,
                altura
            )

        # =====================================================
        # GRÁFICO
        # =====================================================

        if len(self.valores) < 2:
            return

        grafico_pen = QPen(
            Qt.green
        )

        grafico_pen.setWidth(2)

        painter.setPen(
            grafico_pen
        )

        passo = largura / (
            self.quantidade - 1
        )

        for i in range(
            len(self.valores) - 1
        ):

            x1 = int(
                i * passo
            )

            x2 = int(
                (i + 1) * passo
            )

            y1 = int(
                altura
                - (
                    self.valores[i]
                    * altura
                )
            )

            y2 = int(
                altura
                - (
                    self.valores[i + 1]
                    * altura
                )
            )

            painter.drawLine(
                x1,
                y1,
                x2,
                y2
            )

        painter.end()