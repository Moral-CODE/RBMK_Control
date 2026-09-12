from PySide6.QtCore import (
    QTimer,
    Qt
)

from PySide6.QtWidgets import QWidget

from PySide6.QtGui import (
    QColor,
    QPainter
)

import random


class Efeitos(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.parent_widget = parent

        self.setAttribute(
            Qt.WA_TransparentForMouseEvents
        )

        self.opacidade = 0

        self.explodindo = False

        self.frame = 0

        self.timer_animacao = QTimer()

        self.timer_animacao.timeout.connect(
            self.animar_explosao
        )

        # Partículas da explosão
        self.particulas = []

        self.hide()

    # =============================================================
    # INICIAR EXPLOSÃO
    # =============================================================

    def explosao(self):

        self.frame = 0

        self.explodindo = True

        self.opacidade = 255

        self.setGeometry(
            self.parent_widget.rect()
        )

        self.particulas = []

        largura = self.width()
        altura = self.height()

        centro_x = largura // 2
        centro_y = altura // 2

        # =========================================================
        # CRIA PARTÍCULAS
        # =========================================================

        for i in range(110):

            angulo = random.uniform(
                0,
                6.283
            )

            velocidade = random.uniform(
                5,
                30
            )

            self.particulas.append({
                "x": centro_x,
                "y": centro_y,
                "vx": random.uniform(-2, 2),
                "vy": random.uniform(-2, 2),
                "velocidade": velocidade,
                "angulo": angulo,
                "tamanho": random.randint(4, 25),
                "vida": random.randint(25, 60)
            })

        self.show()

        self.raise_()

        self.timer_animacao.start(
            30
        )

        self.update()

    # =============================================================
    # ANIMAÇÃO
    # =============================================================

    def animar_explosao(self):

        self.frame += 1

        # =========================================================
        # FLASH INICIAL
        # =========================================================

        if self.frame <= 5:

            self.opacidade = 255

        elif self.frame <= 18:

            self.opacidade = 220

        else:

            self.opacidade = max(
                0,
                self.opacidade - 12
            )

        # =========================================================
        # PARTÍCULAS
        # =========================================================

        for particula in self.particulas:

            particula["x"] += (
                particula["vx"]
                + random.uniform(-2, 2)
            )

            particula["y"] += (
                particula["vy"]
                + random.uniform(-2, 2)
            )

            particula["vx"] *= 1.04
            particula["vy"] *= 1.04

            particula["vida"] -= 1

        # =========================================================
        # FIM
        # =========================================================

        if self.frame >= 75:

            self.timer_animacao.stop()

            self.explodindo = False

            self.hide()

            return

        self.update()

    # =============================================================
    # DESENHO
    # =============================================================

    def paintEvent(self, event):

        if not self.explodindo:
            return

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing,
            False
        )

        largura = self.width()
        altura = self.height()

        centro_x = largura // 2
        centro_y = altura // 2

        # =========================================================
        # FLASH VERMELHO
        # =========================================================

        painter.fillRect(
            self.rect(),
            QColor(
                255,
                25,
                0,
                min(
                    210,
                    self.opacidade
                )
            )
        )

        # =========================================================
        # NÚCLEO BRANCO
        # =========================================================

        tamanho_nucleo = (
            40
            + self.frame * 45
        )

        alpha_nucleo = max(
            0,
            255 - self.frame * 8
        )

        painter.fillRect(
            centro_x - tamanho_nucleo // 2,
            centro_y - tamanho_nucleo // 2,
            tamanho_nucleo,
            tamanho_nucleo,
            QColor(
                255,
                255,
                210,
                alpha_nucleo
            )
        )

        # =========================================================
        # ONDAS DE CHOQUE
        # =========================================================

        for i in range(4):

            tamanho = (
                self.frame * 55
                - i * 90
            )

            if tamanho <= 0:
                continue

            alpha = max(
                0,
                180
                - self.frame * 5
                - i * 30
            )

            painter.setPen(
                QColor(
                    255,
                    180,
                    30,
                    alpha
                )
            )

            painter.drawRect(
                centro_x - tamanho // 2,
                centro_y - tamanho // 2,
                tamanho,
                tamanho
            )

        # =========================================================
        # PARTÍCULAS
        # =========================================================

        for particula in self.particulas:

            if particula["vida"] <= 0:
                continue

            alpha = min(
                255,
                particula["vida"] * 6
            )

            tamanho = particula["tamanho"]

            tipo = random.randint(
                0,
                2
            )

            if tipo == 0:

                cor = QColor(
                    255,
                    220,
                    80,
                    alpha
                )

            elif tipo == 1:

                cor = QColor(
                    255,
                    100,
                    20,
                    alpha
                )

            else:

                cor = QColor(
                    255,
                    255,
                    180,
                    alpha
                )

            painter.fillRect(
                int(particula["x"]),
                int(particula["y"]),
                tamanho,
                tamanho,
                cor
            )

        # =========================================================
        # RUÍDO / DETRITOS
        # =========================================================

        for i in range(45):

            x = random.randint(
                0,
                max(1, largura - 10)
            )

            y = random.randint(
                0,
                max(1, altura - 10)
            )

            tamanho = random.randint(
                3,
                18
            )

            alpha = random.randint(
                50,
                max(51, self.opacidade)
            )

            painter.fillRect(
                x,
                y,
                tamanho,
                tamanho,
                QColor(
                    255,
                    random.randint(60, 180),
                    0,
                    alpha
                )
            )

        painter.end()