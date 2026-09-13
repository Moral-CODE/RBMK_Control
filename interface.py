from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QProgressBar,
    QGraphicsOpacityEffect
)

from PySide6.QtCore import (
    Qt,
    QTimer,
    QPropertyAnimation,
    QSequentialAnimationGroup,
    QEasingCurve
)

from PySide6.QtGui import (
    QFont,
    QPainter,
    QColor,
    QShortcut,
    QKeySequence
)

import time
import random

from jogo import Jogo
from efeitos import Efeitos
from banco import salvar_partida


# =============================================================
# CONFETES
# =============================================================

class ConfeteWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(
            Qt.WA_TransparentForMouseEvents
        )

        self.particulas = []

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.atualizar
        )

        self.fade = QGraphicsOpacityEffect(
            self
        )

        self.setGraphicsEffect(
            self.fade
        )

        self.fade.setOpacity(
            1.0
        )

    def iniciar(self):

        self.particulas.clear()

        largura = self.width()
        altura = self.height()

        for _ in range(100):

            self.particulas.append({

                "x": random.uniform(
                    0,
                    max(1, largura)
                ),

                "y": random.uniform(
                    -100,
                    0
                ),

                "vx": random.uniform(
                    -3,
                    3
                ),

                "vy": random.uniform(
                    2,
                    7
                ),

                "gravidade": random.uniform(
                    0.08,
                    0.18
                ),

                "tamanho": random.randint(
                    4,
                    9
                ),

                "rotacao": random.randint(
                    0,
                    360
                ),

                "rotacao_vel": random.uniform(
                    -8,
                    8
                ),

                "cor": random.choice([
                    "#ff2222",
                    "#ffaa00",
                    "#00ff66",
                    "#00aaff",
                    "#ffffff",
                    "#ff44cc"
                ])
            })

        self.fade.setOpacity(
            1.0
        )

        self.show()
        self.raise_()

        self.timer.start(
            16
        )

        QTimer.singleShot(
            3000,
            self.fade_out
        )

    def atualizar(self):

        vivos = []

        for p in self.particulas:

            p["x"] += p["vx"]
            p["y"] += p["vy"]

            p["vy"] += p["gravidade"]

            p["rotacao"] += p["rotacao_vel"]

            if p["y"] < self.height() + 30:

                vivos.append(
                    p
                )

        self.particulas = vivos

        self.update()

        if not self.particulas:

            self.timer.stop()

            self.hide()

    def fade_out(self):

        animacao = QPropertyAnimation(
            self.fade,
            b"opacity",
            self
        )

        animacao.setDuration(
            1000
        )

        animacao.setStartValue(
            self.fade.opacity()
        )

        animacao.setEndValue(
            0
        )

        animacao.setEasingCurve(
            QEasingCurve.OutCubic
        )

        animacao.finished.connect(
            self.parar
        )

        self.animacao_fade = animacao

        animacao.start()

    def parar(self):

        self.timer.stop()

        self.hide()

        self.particulas.clear()

        self.fade.setOpacity(
            1.0
        )

    def paintEvent(self, event):

        painter = QPainter(
            self
        )

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        for p in self.particulas:

            painter.save()

            painter.translate(
                p["x"],
                p["y"]
            )

            painter.rotate(
                p["rotacao"]
            )

            painter.setBrush(
                QColor(
                    p["cor"]
                )
            )

            painter.setPen(
                Qt.NoPen
            )

            painter.drawRect(
                0,
                0,
                p["tamanho"],
                p["tamanho"] * 2
            )

            painter.restore()


# =============================================================
# INTERFACE
# =============================================================

class Interface(QWidget):

    def __init__(self):

        super().__init__()

        # =========================================================
        # ATALHOS
        # =========================================================

        self.shortcut_space = QShortcut(
            QKeySequence("Space"),
            self
        )

        self.shortcut_space.setContext(
            Qt.ApplicationShortcut
        )

        self.shortcut_space.activated.connect(
            self.tecla_space
        )

        self.shortcut_enter = QShortcut(
            QKeySequence("Enter"),
            self
        )

        self.shortcut_enter.setContext(
            Qt.ApplicationShortcut
        )

        self.shortcut_enter.activated.connect(
            self.tecla_enter
        )

        self.setFocusPolicy(
            Qt.StrongFocus
        )

        self.setFocus()

        # =========================================================
        # JOGO
        # =========================================================

        self.jogo = Jogo()

        self.efeitos = Efeitos(
            self
        )

        self.setWindowTitle(
            "RBMK-1000 // SISTEMA DE CONTROLE"
        )

        self.showMaximized()

        self.modo = "inicio"

        # =========================================================
        # FONTES
        # =========================================================

        self.fonte_titulo = QFont(
            "Courier New",
            25,
            QFont.Bold
        )

        self.fonte_normal = QFont(
            "Courier New",
            14
        )

        self.fonte_pequena = QFont(
            "Courier New",
            11
        )

        self.fonte_timer = QFont(
            "Press Start 2P",
            62,
            QFont.Bold
        )

        self.fonte_grafico = QFont(
            "Courier New",
            11
        )

        self.fonte_credito = QFont(
            "Courier New",
            12,
            QFont.Bold
        )

        # =========================================================
        # CORES
        # =========================================================

        self.verde = "#00ff66"
        self.vermelho = "#ff2222"
        self.amarelo = "#ffaa00"
        self.branco = "#dddddd"

        # =========================================================
        # TÍTULO
        # =========================================================

        self.titulo = QLabel(
            "RBMK-1000 // UNIDADE 4"
        )

        self.titulo.setAlignment(
            Qt.AlignCenter
        )

        self.titulo.setFont(
            self.fonte_titulo
        )

        self.subtitulo = QLabel(
            "SISTEMA DE CONTROLE DO REATOR NUCLEAR"
        )

        self.subtitulo.setAlignment(
            Qt.AlignCenter
        )

        self.subtitulo.setFont(
            self.fonte_pequena
        )

        # =========================================================
        # STATUS
        # =========================================================

        self.status = QLabel(
            "● SISTEMA OFFLINE"
        )

        self.status.setAlignment(
            Qt.AlignCenter
        )

        self.status.setFont(
            self.fonte_normal
        )

        # =========================================================
        # TIMER
        # =========================================================

        self.timer_label = QLabel(
            "00.00"
        )

        self.timer_label.setAlignment(
            Qt.AlignCenter
        )

        self.timer_label.setFont(
            self.fonte_timer
        )

        self.alvo = QLabel(
            "SISTEMA EM ESPERA"
        )

        self.alvo.setAlignment(
            Qt.AlignCenter
        )

        self.alvo.setFont(
            self.fonte_normal
        )

        self.painel_timer = QFrame()

        timer_layout = QVBoxLayout()

        timer_layout.addStretch()

        timer_layout.addWidget(
            self.timer_label
        )

        timer_layout.addWidget(
            self.alvo
        )

        timer_layout.addStretch()

        self.painel_timer.setLayout(
            timer_layout
        )

        # =========================================================
        # ESTATÍSTICAS
        # =========================================================

        self.estatisticas = QFrame()

        stats_layout = QVBoxLayout()

        self.stat_tentativas = QLabel(
            "TENTATIVAS : 0"
        )

        self.stat_acertos = QLabel(
            "ACERTOS    : 0"
        )

        self.stat_erros = QLabel(
            "ERROS      : 0"
        )

        self.stat_precisao = QLabel(
            "PRECISÃO   : 0%"
        )

        self.stat_perfeitos = QLabel(
            "CRAVADOS   : 0"
        )

        for label in (
            self.stat_tentativas,
            self.stat_acertos,
            self.stat_erros,
            self.stat_precisao,
            self.stat_perfeitos
        ):

            label.setFont(
                self.fonte_pequena
            )

            stats_layout.addWidget(
                label
            )

        self.estatisticas.setLayout(
            stats_layout
        )

        # =========================================================
        # TEMPERATURA
        # =========================================================

        self.temp_valor = QLabel(
            "280 °C"
        )

        self.temp_valor.setFont(
            self.fonte_normal
        )

        self.temp_grafico = QLabel(
            "▁▂▃▂▃▅▄▅▆▅▇"
        )

        self.temp_grafico.setFont(
            self.fonte_grafico
        )

        self.temp_barra = QProgressBar()

        self.temp_barra.setRange(
            0,
            100
        )

        self.temp_barra.setValue(
            20
        )

        self.temp_barra.setTextVisible(
            False
        )

        painel_temp = QFrame()

        temp_layout = QVBoxLayout()

        temp_layout.addWidget(
            QLabel(
                "TEMPERATURA DO NÚCLEO"
            )
        )

        temp_layout.addWidget(
            self.temp_valor
        )

        temp_layout.addWidget(
            self.temp_grafico
        )

        temp_layout.addWidget(
            self.temp_barra
        )

        painel_temp.setLayout(
            temp_layout
        )

        # =========================================================
        # RADIAÇÃO
        # =========================================================

        self.radiacao_valor = QLabel(
            "BAIXA"
        )

        self.radiacao_valor.setFont(
            self.fonte_normal
        )

        self.radiacao_barra = QProgressBar()

        self.radiacao_barra.setRange(
            0,
            100
        )

        self.radiacao_barra.setValue(
            10
        )

        self.radiacao_barra.setTextVisible(
            False
        )

        painel_radiacao = QFrame()

        radiacao_layout = QVBoxLayout()

        radiacao_layout.addWidget(
            QLabel(
                "NÍVEL DE RADIAÇÃO"
            )
        )

        radiacao_layout.addWidget(
            self.radiacao_valor
        )

        radiacao_layout.addWidget(
            self.radiacao_barra
        )

        painel_radiacao.setLayout(
            radiacao_layout
        )

        # =========================================================
        # POTÊNCIA
        # =========================================================

        self.potencia_valor = QLabel(
            "20%"
        )

        self.potencia_valor.setFont(
            self.fonte_normal
        )

        self.potencia_barra = QProgressBar()

        self.potencia_barra.setRange(
            0,
            100
        )

        self.potencia_barra.setValue(
            20
        )

        self.potencia_barra.setTextVisible(
            False
        )

        painel_potencia = QFrame()

        potencia_layout = QVBoxLayout()

        potencia_layout.addWidget(
            QLabel(
                "SAÍDA DE POTÊNCIA"
            )
        )

        potencia_layout.addWidget(
            self.potencia_valor
        )

        potencia_layout.addWidget(
            self.potencia_barra
        )

        painel_potencia.setLayout(
            potencia_layout
        )

        # =========================================================
        # RESFRIAMENTO
        # =========================================================

        self.cooling_valor = QLabel(
            "95%"
        )

        self.cooling_valor.setFont(
            self.fonte_normal
        )

        self.cooling_barra = QProgressBar()

        self.cooling_barra.setRange(
            0,
            100
        )

        self.cooling_barra.setValue(
            95
        )

        self.cooling_barra.setTextVisible(
            False
        )

        painel_cooling = QFrame()

        cooling_layout = QVBoxLayout()

        cooling_layout.addWidget(
            QLabel(
                "SISTEMA DE RESFRIAMENTO"
            )
        )

        cooling_layout.addWidget(
            self.cooling_valor
        )

        cooling_layout.addWidget(
            self.cooling_barra
        )

        painel_cooling.setLayout(
            cooling_layout
        )

        # =========================================================
        # INDICADORES
        # =========================================================

        self.indicador_core = QLabel(
            "● NÚCLEO"
        )

        self.indicador_cooling = QLabel(
            "● RESFRIAMENTO"
        )

        self.indicador_control = QLabel(
            "● CONTROLE"
        )

        for indicador in (
            self.indicador_core,
            self.indicador_cooling,
            self.indicador_control
        ):

            indicador.setFont(
                self.fonte_pequena
            )

            indicador.setAlignment(
                Qt.AlignCenter
            )

        indicadores = QFrame()

        indicadores_layout = QHBoxLayout()

        indicadores_layout.addWidget(
            self.indicador_core
        )

        indicadores_layout.addWidget(
            self.indicador_cooling
        )

        indicadores_layout.addWidget(
            self.indicador_control
        )

        indicadores.setLayout(
            indicadores_layout
        )

        # =========================================================
        # ALERTA
        # =========================================================

        self.alerta = QLabel(
            "SISTEMA PRONTO"
        )

        self.alerta.setAlignment(
            Qt.AlignCenter
        )

        self.alerta.setFont(
            self.fonte_normal
        )

        # =========================================================
        # INSTRUÇÃO
        # =========================================================

        self.instrucao = QLabel(
            "PRESSIONE ENTER PARA INICIALIZAR"
        )

        self.instrucao.setAlignment(
            Qt.AlignCenter
        )

        self.instrucao.setFont(
            self.fonte_normal
        )

        # =========================================================
        # CRÉDITO
        # =========================================================

        self.credito = QLabel(
            "Criado por: Moral ☕"
        )

        self.credito.setAlignment(
            Qt.AlignRight
        )

        self.credito.setFont(
            self.fonte_credito
        )

        # =========================================================
        # LAYOUT
        # =========================================================

        topo = QVBoxLayout()

        topo.addWidget(
            self.titulo
        )

        topo.addWidget(
            self.subtitulo
        )

        topo.addWidget(
            self.status
        )

        esquerda = QVBoxLayout()

        esquerda.addWidget(
            painel_temp
        )

        esquerda.addWidget(
            painel_potencia
        )

        esquerda.addWidget(
            self.estatisticas
        )

        direita = QVBoxLayout()

        direita.addWidget(
            painel_radiacao
        )

        direita.addWidget(
            painel_cooling
        )

        direita.addWidget(
            indicadores
        )

        centro = QVBoxLayout()

        centro.addWidget(
            self.painel_timer,
            1
        )

        centro.addWidget(
            self.alerta
        )

        centro.addWidget(
            self.instrucao
        )

        hud = QHBoxLayout()

        hud.addLayout(
            esquerda,
            1
        )

        hud.addLayout(
            centro,
            2
        )

        hud.addLayout(
            direita,
            1
        )

        layout = QVBoxLayout()

        layout.setContentsMargins(
            20,
            15,
            20,
            10
        )

        layout.addLayout(
            topo
        )

        layout.addLayout(
            hud,
            1
        )

        layout.addWidget(
            self.credito
        )

        self.setLayout(
            layout
        )

        # =========================================================
        # OVERLAY DE ALERTA
        # =========================================================

        self.flash_alerta = QLabel(
            self
        )

        self.flash_alerta.setGeometry(
            self.rect()
        )

        self.flash_alerta.setAttribute(
            Qt.WA_TransparentForMouseEvents
        )

        self.flash_alerta.hide()

        self.flash_opacidade = QGraphicsOpacityEffect(
            self.flash_alerta
        )

        self.flash_alerta.setGraphicsEffect(
            self.flash_opacidade
        )

        self.flash_animacao = None

        # =========================================================
        # OVERLAY DE MORTE
        # =========================================================

        self.overlay_morte = None
        self.erro_morte = None
        self.retry_morte = None

        self.morte_timer = QTimer(
            self
        )

        self.morte_timer.timeout.connect(
            self.animar_morte
        )

        self.morte_estado = True

        # =========================================================
        # CONFETES
        # =========================================================

        self.confetes = ConfeteWidget(
            self
        )

        self.confetes.hide()

        # =========================================================
        # ESTATÍSTICAS
        # =========================================================

        self.tentativas = 0
        self.acertos = 0
        self.erros = 0
        self.perfeitos = 0

        # =========================================================
        # TIMER PRINCIPAL
        # =========================================================

        self.timer = QTimer(
            self
        )

        self.timer.timeout.connect(
            self.atualizar_timer
        )

        # =========================================================
        # LIMITE ABSOLUTO DE 10 SEGUNDOS
        # =========================================================

        self.limite_timer = QTimer(
            self
        )

        self.limite_timer.setSingleShot(
            True
        )

        self.limite_timer.timeout.connect(
            self.tempo_esgotado
        )

        # =========================================================
        # TIMER DO HUD
        # =========================================================

        self.hud_timer = QTimer(
            self
        )

        self.hud_timer.timeout.connect(
            self.animar_hud
        )

        self.hud_timer.start(
            120
        )

        # =========================================================
        # ESTILO
        # =========================================================

        self.setStyleSheet("""
            QWidget {
                background-color: #050505;
                color: #dddddd;
            }

            QFrame {
                background-color: #0b0b0b;
                border: 2px solid #333333;
                border-radius: 3px;
            }

            QLabel {
                color: #dddddd;
            }

            QProgressBar {
                background-color: #111111;
                border: 1px solid #444444;
                height: 9px;
            }

            QProgressBar::chunk {
                background-color: #00aa44;
            }
        """)

        self.mudar_cor(
            self.branco
        )

    # =============================================================
    # REDIMENSIONAMENTO
    # =============================================================

    def resizeEvent(
        self,
        event
    ):

        super().resizeEvent(
            event
        )

        if hasattr(
            self,
            "flash_alerta"
        ):

            self.flash_alerta.setGeometry(
                self.rect()
            )

        if hasattr(
            self,
            "overlay_morte"
        ) and self.overlay_morte:

            self.overlay_morte.setGeometry(
                self.rect()
            )

        if hasattr(
            self,
            "confetes"
        ):

            self.confetes.setGeometry(
                self.rect()
            )

    # =============================================================
    # COR
    # =============================================================

    def mudar_cor(
        self,
        cor
    ):

        widgets = (
            self.timer_label,
            self.status,
            self.alerta,
            self.instrucao,
            self.alvo,
            self.indicador_core,
            self.indicador_cooling,
            self.indicador_control
        )

        for widget in widgets:

            widget.setStyleSheet(
                f"color: {cor};"
            )

    # =============================================================
    # FLASH
    # =============================================================

    def flash_emergencia(
        self,
        cor,
        intensidade=0.28
    ):

        self.flash_alerta.setStyleSheet(
            f"""
            background-color: {cor};
            """
        )

        self.flash_alerta.raise_()

        self.flash_opacidade.setOpacity(
            0
        )

        self.flash_alerta.show()

        self.flash_animacao = (
            QSequentialAnimationGroup(
                self
            )
        )

        entrada = QPropertyAnimation(
            self.flash_opacidade,
            b"opacity"
        )

        entrada.setDuration(
            100
        )

        entrada.setStartValue(
            0
        )

        entrada.setEndValue(
            intensidade
        )

        saida = QPropertyAnimation(
            self.flash_opacidade,
            b"opacity"
        )

        saida.setDuration(
            420
        )

        saida.setStartValue(
            intensidade
        )

        saida.setEndValue(
            0
        )

        self.flash_animacao.addAnimation(
            entrada
        )

        self.flash_animacao.addAnimation(
            saida
        )

        self.flash_animacao.finished.connect(
            self.flash_alerta.hide
        )

        self.flash_animacao.start()

    # =============================================================
    # HUD
    # =============================================================

    def animar_hud(self):

        if self.modo not in (
            "jogando",
            "pronto",
            "alertas"
        ):

            return

        if self.modo == "pronto":

            self.temp_valor.setText(
                "280 °C"
            )

            self.potencia_valor.setText(
                "20%"
            )

            self.cooling_valor.setText(
                "95%"
            )

            self.radiacao_valor.setText(
                "BAIXA"
            )

            return

        if self.modo == "alertas":

            quantidade_alertas = 6

            indice = getattr(
                self,
                "indice_alerta",
                0
            )

            progresso = (
                indice /
                quantidade_alertas
            )

            ruido = random.uniform(
                -8,
                8
            )

            temperatura = (
                280
                + progresso * 420
                + ruido
            )

            potencia = (
                20
                + progresso * 80
                + random.uniform(
                    -8,
                    8
                )
            )

            cooling = (
                96
                - progresso * 70
                + random.uniform(
                    -6,
                    6
                )
            )

            radiacao = (
                8
                + progresso * 92
                + random.uniform(
                    -6,
                    6
                )
            )

            temperatura = max(
                280,
                temperatura
            )

            potencia = max(
                0,
                min(
                    100,
                    potencia
                )
            )

            cooling = max(
                10,
                min(
                    100,
                    cooling
                )
            )

            radiacao = max(
                0,
                min(
                    100,
                    radiacao
                )
            )

            self.temp_valor.setText(
                f"{temperatura:.0f} °C"
            )

            self.potencia_valor.setText(
                f"{potencia:.0f}%"
            )

            self.cooling_valor.setText(
                f"{cooling:.0f}%"
            )

            if radiacao >= 85:

                texto = "CRÍTICA"

            elif radiacao >= 65:

                texto = "ALTA"

            elif radiacao >= 40:

                texto = "ELEVADA"

            else:

                texto = "BAIXA"

            self.radiacao_valor.setText(
                texto
            )

            self.temp_barra.setValue(
                int(
                    min(
                        100,
                        temperatura / 5
                    )
                )
            )

            self.potencia_barra.setValue(
                int(potencia)
            )

            self.cooling_barra.setValue(
                int(cooling)
            )

            self.radiacao_barra.setValue(
                int(radiacao)
            )

            blocos = [
                "▁",
                "▂",
                "▃",
                "▄",
                "▅",
                "▆",
                "▇",
                "█"
            ]

            grafico = ""

            for _ in range(14):

                base = progresso * 6

                variacao = random.uniform(
                    0,
                    4
                )

                indice = int(
                    base + variacao
                )

                indice = max(
                    0,
                    min(
                        7,
                        indice
                    )
                )

                grafico += blocos[
                    indice
                ]

            self.temp_grafico.setText(
                grafico
            )

            if progresso < 0.50:

                self.mudar_cor(
                    self.amarelo
                )

                self.indicador_core.setStyleSheet(
                    f"color: {self.amarelo};"
                )

                self.indicador_cooling.setStyleSheet(
                    f"color: {self.verde};"
                )

                self.indicador_control.setStyleSheet(
                    f"color: {self.verde};"
                )

            elif progresso < 0.80:

                self.mudar_cor(
                    self.amarelo
                )

                self.indicador_core.setStyleSheet(
                    f"color: {self.amarelo};"
                )

                self.indicador_cooling.setStyleSheet(
                    f"color: {self.amarelo};"
                )

                self.indicador_control.setStyleSheet(
                    f"color: {self.amarelo};"
                )

            else:

                self.mudar_cor(
                    self.vermelho
                )

                self.indicador_core.setStyleSheet(
                    f"color: {self.vermelho};"
                )

                self.indicador_cooling.setStyleSheet(
                    f"color: {self.vermelho};"
                )

                self.indicador_control.setStyleSheet(
                    f"color: {self.vermelho};"
                )

            return

        tempo = (
            time.perf_counter()
            - self.jogo.tempo_inicio
        )

        alvo = max(
            0.01,
            self.jogo.tempo_alvo
        )

        progresso = (
            tempo / alvo
        )

        ruido = random.uniform(
            -2.5,
            2.5
        )

        temperatura = (
            280
            + progresso * 260
            + ruido
        )

        potencia = (
            20
            + progresso * 80
            + random.uniform(
                -3,
                3
            )
        )

        cooling = (
            96
            - progresso * 40
            + random.uniform(
                -2,
                2
            )
        )

        radiacao = (
            8
            + progresso * 90
            + random.uniform(
                -3,
                3
            )
        )

        temperatura = max(
            280,
            temperatura
        )

        potencia = max(
            0,
            min(
                100,
                potencia
            )
        )

        cooling = max(
            20,
            min(
                100,
                cooling
            )
        )

        radiacao = max(
            0,
            min(
                100,
                radiacao
            )
        )

        self.temp_valor.setText(
            f"{temperatura:.0f} °C"
        )

        self.potencia_valor.setText(
            f"{potencia:.0f}%"
        )

        self.cooling_valor.setText(
            f"{cooling:.0f}%"
        )

        if radiacao >= 85:

            texto = "CRÍTICA"

        elif radiacao >= 65:

            texto = "ALTA"

        elif radiacao >= 40:

            texto = "ELEVADA"

        else:

            texto = "BAIXA"

        self.radiacao_valor.setText(
            texto
        )

        self.temp_barra.setValue(
            int(
                min(
                    100,
                    temperatura / 5
                )
            )
        )

        self.potencia_barra.setValue(
            int(potencia)
        )

        self.cooling_barra.setValue(
            int(cooling)
        )

        self.radiacao_barra.setValue(
            int(radiacao)
        )

        blocos = [
            "▁",
            "▂",
            "▃",
            "▄",
            "▅",
            "▆",
            "▇",
            "█"
        ]

        grafico = ""

        for _ in range(14):

            base = progresso * 6

            variacao = random.uniform(
                0,
                2.5
            )

            indice = int(
                base + variacao
            )

            indice = max(
                0,
                min(
                    7,
                    indice
                )
            )

            grafico += blocos[
                indice
            ]

        self.temp_grafico.setText(
            grafico
        )

        if progresso < 0.50:

            self.mudar_cor(
                self.amarelo
            )

            self.status.setText(
                "● NÚCLEO ATIVO"
            )

            self.alerta.setText(
                "SISTEMA OPERANDO"
            )

            self.indicador_core.setStyleSheet(
                f"color: {self.amarelo};"
            )

            self.indicador_cooling.setStyleSheet(
                f"color: {self.verde};"
            )

            self.indicador_control.setStyleSheet(
                f"color: {self.verde};"
            )

        elif progresso < 0.75:

            self.mudar_cor(
                self.amarelo
            )

            self.status.setText(
                "● AVISO DO SISTEMA"
            )

            self.alerta.setText(
                "⚠ INSTABILIDADE DO REATOR DETECTADA"
            )

            self.indicador_core.setStyleSheet(
                f"color: {self.amarelo};"
            )

            self.indicador_cooling.setStyleSheet(
                f"color: {self.amarelo};"
            )

            self.indicador_control.setStyleSheet(
                f"color: {self.verde};"
            )

        elif progresso < 0.90:

            self.mudar_cor(
                self.vermelho
            )

            self.status.setText(
                "● CONDIÇÃO CRÍTICA"
            )

            self.alerta.setText(
                "⚠⚠ TEMPERATURA DO NÚCLEO SUBINDO ⚠⚠"
            )

            self.indicador_core.setStyleSheet(
                f"color: {self.vermelho};"
            )

            self.indicador_cooling.setStyleSheet(
                f"color: {self.vermelho};"
            )

            self.indicador_control.setStyleSheet(
                f"color: {self.amarelo};"
            )

        else:

            self.mudar_cor(
                self.vermelho
            )

            self.status.setText(
                "●☢ FALHA CRÍTICA ☢●"
            )

            self.alerta.setText(
                "!!! FALHA DO REATOR IMINENTE !!!"
            )

            self.indicador_core.setStyleSheet(
                f"color: {self.vermelho};"
            )

            self.indicador_cooling.setStyleSheet(
                f"color: {self.vermelho};"
            )

            self.indicador_control.setStyleSheet(
                f"color: {self.vermelho};"
            )

    # =============================================================
    # ENTER
    # =============================================================

    def tecla_enter(self):

        if self.modo == "inicio":

            self.iniciar_alertas()

        elif self.modo == "morte":

            self.reiniciar_jogo()

        elif self.modo == "resultado":

            self.reiniciar_jogo()

    # =============================================================
    # SPACE
    # =============================================================

    def tecla_space(self):

        if self.modo == "pronto":

            self.iniciar_jogo()

        elif self.modo == "jogando":

            self.parar_jogo()

    # =============================================================
    # FALLBACK DE TECLADO
    # =============================================================

    def keyPressEvent(
        self,
        event
    ):

        if event.key() in (
            Qt.Key_Return,
            Qt.Key_Enter
        ):

            self.tecla_enter()

            event.accept()

            return

        if event.key() == Qt.Key_Space:

            self.tecla_space()

            event.accept()

            return

        super().keyPressEvent(
            event
        )

    # =============================================================
    # ALERTAS
    # =============================================================

    def iniciar_alertas(self):

        self.modo = "alertas"

        self.mudar_cor(
            self.amarelo
        )

        self.titulo.setText(
            "RBMK-1000 // INICIALIZAÇÃO"
        )

        self.status.setText(
            "● INICIALIZAÇÃO DO SISTEMA"
        )

        self.instrucao.setText(
            "AGUARDE..."
        )

        self.alertas = [

            "INICIALIZANDO SISTEMA...",

            "SISTEMA DE RESFRIAMENTO: AVISO",

            "BARRAS DE CONTROLE: VERIFICAÇÃO NECESSÁRIA",

            "NÚCLEO DO REATOR: INSTÁVEL",

            "NÍVEL DE RADIAÇÃO: ALTO",

            "FALHA CRÍTICA DO REATOR"
        ]

        self.indice_alerta = 0

        self.timer_alertas = QTimer(
            self
        )

        self.timer_alertas.timeout.connect(
            self.mostrar_alerta
        )

        self.timer_alertas.start(
            600
        )

        self.mostrar_alerta()

    # =============================================================
    # MOSTRAR ALERTA
    # =============================================================

    def mostrar_alerta(self):

        if self.indice_alerta >= len(
            self.alertas
        ):

            self.timer_alertas.stop()

            self.modo = "pronto"

            self.titulo.setText(
                "RBMK-1000 // CONTROLE DE EMERGÊNCIA"
            )

            self.status.setText(
                "● SISTEMA CRÍTICO"
            )

            self.alerta.setText(
                "⚠ INSTABILIDADE DO REATOR DETECTADA ⚠"
            )

            self.instrucao.setText(
                "PRESSIONE ESPAÇO PARA COMEÇAR"
            )

            return

        self.alerta.setText(
            self.alertas[
                self.indice_alerta
            ]
        )

        if self.indice_alerta < 2:

            self.flash_emergencia(
                self.amarelo,
                0.20
            )

        elif self.indice_alerta < 4:

            self.flash_emergencia(
                self.amarelo,
                0.28
            )

        else:

            self.flash_emergencia(
                self.vermelho,
                0.38
            )

        self.indice_alerta += 1

    # =============================================================
    # INICIAR JOGO
    # =============================================================

    def iniciar_jogo(self):

        self.setFocus()

        self.jogo.novo_desafio()

        self.jogo.iniciar()

        self.modo = "jogando"

        self.tentativas += 1

        self.mudar_cor(
            self.amarelo
        )

        self.titulo.setText(
            "RBMK-1000 // REATOR ATIVO"
        )

        self.status.setText(
            "● NÚCLEO ATIVO // CRÍTICO"
        )

        self.alvo.setText(
            f"ALVO: {self.jogo.tempo_alvo:.1f} SEG"
        )

        self.timer_label.setText(
            "00.00"
        )

        self.alerta.setText(
            "⚠ ESTABILIZE O REATOR ⚠"
        )

        self.instrucao.setText(
            "PRESSIONE ESPAÇO PARA PARAR"
        )

        # Timer visual
        self.timer.start(
            10
        )

        # =========================================================
        # LIMITE MÁXIMO DE 10 SEGUNDOS
        # =========================================================

        self.limite_timer.start(
            10000
        )

        self.atualizar_estatisticas()

    # =============================================================
    # TIMER
    # =============================================================

    def atualizar_timer(self):

        if not self.jogo.rodando:

            return

        tempo = (
            time.perf_counter()
            - self.jogo.tempo_inicio
        )

        self.timer_label.setText(
            f"{tempo:05.2f}"
        )

        alvo = self.jogo.tempo_alvo

        progresso = (
            tempo / alvo
        )

        if progresso >= 1.0:

            self.status.setText(
                "●☢ SOBRECARGA ☢●"
            )

            self.alerta.setText(
                "!!! REATOR ALÉM DO LIMITE SEGURO !!!"
            )

            self.mudar_cor(
                self.vermelho
            )

            if int(
                tempo * 15
            ) % 2 == 0:

                self.timer_label.setStyleSheet("""
                    color: #ffffff;
                    background-color: #770000;
                """)

            else:

                self.timer_label.setStyleSheet(
                    f"""
                    color: {self.vermelho};
                    background-color: #220000;
                    """
                )

            return

        if progresso < 0.50:

            self.mudar_cor(
                self.amarelo
            )

            self.status.setText(
                "● NÚCLEO ATIVO"
            )

            self.alerta.setText(
                "SISTEMA OPERANDO"
            )

        elif progresso < 0.75:

            self.mudar_cor(
                self.amarelo
            )

            self.status.setText(
                "● AVISO DO SISTEMA"
            )

            self.alerta.setText(
                "⚠ INSTABILIDADE DO REATOR DETECTADA"
            )

        elif progresso < 0.90:

            self.mudar_cor(
                self.vermelho
            )

            self.status.setText(
                "● CONDIÇÃO CRÍTICA"
            )

            self.alerta.setText(
                "⚠⚠ TEMPERATURA DO NÚCLEO SUBINDO ⚠⚠"
            )

        else:

            self.mudar_cor(
                self.vermelho
            )

            self.status.setText(
                "●☢ FALHA CRÍTICA ☢●"
            )

            self.alerta.setText(
                "!!! FALHA DO REATOR IMINENTE !!!"
            )

            if int(
                tempo * 10
            ) % 2 == 0:

                self.timer_label.setStyleSheet(
                    f"""
                    color: {self.vermelho};
                    background-color: #330000;
                    """
                )

            else:

                self.timer_label.setStyleSheet("""
                    color: #ffffff;
                    background-color: #550000;
                """)

    # =============================================================
    # TEMPO ESGOTADO
    # =============================================================

    def tempo_esgotado(self):

        # Se o jogador já terminou a partida,
        # não fazemos absolutamente nada.

        if self.modo != "jogando":

            return

        if not self.jogo.rodando:

            return

        # Para o timer visual
        self.timer.stop()

        # Impede que o limite seja chamado novamente
        self.limite_timer.stop()

        # Calcula o resultado real da partida
        resultado = self.jogo.parar()

        if resultado is None:

            return

        # Força o estado de erro
        resultado["acertou"] = False

        # Conta como erro
        self.erros += 1

        # Salva normalmente no banco
        salvar_partida(
            resultado["tempo_alvo"],
            resultado["tempo_jogador"],
            resultado["acertou"]
        )

        self.atualizar_estatisticas()

        # Mostra exatamente a mesma sequência
        # de explosão usada em uma derrota normal.
        self.mostrar_resultado(
            resultado
        )

    # =============================================================
    # PARAR JOGO
    # =============================================================

    def parar_jogo(self):

        if self.modo != "jogando":

            return

        # Para o timer visual
        self.timer.stop()

        # MUITO IMPORTANTE:
        # se o jogador apertou Space antes dos 10s,
        # o limite automático precisa ser cancelado.
        self.limite_timer.stop()

        resultado = self.jogo.parar()

        if resultado is None:

            return

        salvar_partida(
            resultado["tempo_alvo"],
            resultado["tempo_jogador"],
            resultado["acertou"]
        )

        if resultado["acertou"]:

            self.modo = "resultado"

            self.mudar_cor(
                self.verde
            )

            self.status.setText(
                "● REATOR ESTABILIZADO"
            )

            self.titulo.setText(
                "RBMK-1000 // ESTABILIZAÇÃO COMPLETA"
            )

            self.subtitulo.setText(
                "SUCESSO DO OPERADOR"
            )

            self.alerta.setText(
                "✓ REATOR ESTÁVEL ✓"
            )

            self.instrucao.setText(
                "PRESSIONE ENTER PARA RETORNAR"
            )

            self.acertos += 1

            if resultado["diferenca"] <= 0.03:

                self.perfeitos += 1

                self.mostrar_cravado()

                self.alerta.setText(
                    "WOW, CRAVADO! PARABÉNS!"
                )

                self.instrucao.setText(
                    "TEMPO PERFEITO // PRESSIONE ENTER"
                )

        else:

            self.erros += 1

        self.atualizar_estatisticas()

        self.mostrar_resultado(
            resultado
        )

    # =============================================================
    # CRAVADO
    # =============================================================

    def mostrar_cravado(self):

        aviso = QLabel(
            "WOW - CRAVOU 🥇",
            self
        )

        aviso.setAlignment(
            Qt.AlignCenter
        )

        aviso.setFont(
            QFont(
                "Courier New",
                34,
                QFont.Bold
            )
        )

        aviso.setStyleSheet("""
            QLabel {
                color: #ffdd00;
                background-color: rgba(0, 0, 0, 100);
                padding: 20px;
            }
        """)

        aviso.setGeometry(
            0,
            0,
            self.width(),
            self.height()
        )

        efeito = QGraphicsOpacityEffect(
            aviso
        )

        aviso.setGraphicsEffect(
            efeito
        )

        efeito.setOpacity(
            1.0
        )

        aviso.raise_()

        aviso.show()

        self.confetes.setGeometry(
            self.rect()
        )

        self.confetes.raise_()

        self.confetes.iniciar()

        animacao = QPropertyAnimation(
            efeito,
            b"opacity",
            aviso
        )

        animacao.setDuration(
            1600
        )

        animacao.setStartValue(
            1.0
        )

        animacao.setEndValue(
            0.0
        )

        animacao.setEasingCurve(
            QEasingCurve.OutCubic
        )

        def remover():

            aviso.hide()

            aviso.deleteLater()

        animacao.finished.connect(
            remover
        )

        aviso._animacao = animacao

        animacao.start()

    # =============================================================
    # ESTATÍSTICAS
    # =============================================================

    def atualizar_estatisticas(self):

        if self.tentativas > 0:

            precisao = (
                self.acertos /
                self.tentativas
            ) * 100

        else:

            precisao = 0

        self.stat_tentativas.setText(
            f"TENTATIVAS : {self.tentativas}"
        )

        self.stat_acertos.setText(
            f"ACERTOS    : {self.acertos}"
        )

        self.stat_erros.setText(
            f"ERROS      : {self.erros}"
        )

        self.stat_precisao.setText(
            f"PRECISÃO   : {precisao:.0f}%"
        )

        self.stat_perfeitos.setText(
            f"CRAVADOS   : {self.perfeitos}"
        )

    # =============================================================
    # RESULTADO
    # =============================================================

    def mostrar_resultado(
        self,
        resultado
    ):

        self.timer_label.setText(
            f"{resultado['tempo_jogador']:05.2f}"
        )

        if resultado["acertou"]:

            self.modo = "resultado"

            self.mudar_cor(
                self.verde
            )

            self.status.setText(
                "● REATOR ESTABILIZADO"
            )

            if resultado["diferenca"] <= 0.03:

                self.alerta.setText(
                    "WOW, CRAVADO! PARABÉNS!"
                )

                self.instrucao.setText(
                    "TEMPO PERFEITO // PRESSIONE ENTER"
                )

            else:

                self.alerta.setText(
                    "✓ REATOR ESTÁVEL ✓"
                )

                self.instrucao.setText(
                    "PRESSIONE ENTER PARA RETORNAR"
                )

        else:

            self.modo = "explodindo"

            self.mudar_cor(
                self.vermelho
            )

            self.status.setText(
                "● FALHA DO REATOR"
            )

            self.alerta.setText(
                "☢ FALHA CRÍTICA DO NÚCLEO ☢"
            )

            self.instrucao.setText(
                "EVACUE IMEDIATAMENTE"
            )

            QTimer.singleShot(
                350,
                self.iniciar_explosao
            )

    # =============================================================
    # EXPLOSÃO
    # =============================================================

    def iniciar_explosao(self):

        if self.modo != "explodindo":

            return

        self.titulo.setText(
            "!!! FALHA CRÍTICA !!!"
        )

        self.subtitulo.setText(
            "RUPTURA DO NÚCLEO DO REATOR"
        )

        self.status.setText(
            "☢☢☢ EXPLOSÃO ☢☢☢"
        )

        self.alerta.setText(
            "!!! NÚCLEO DESTRUTIVO !!!"
        )

        self.efeitos.explosao()

        QTimer.singleShot(
            2200,
            self.tela_morte
        )

    # =============================================================
    # ANIMAÇÃO DA MORTE
    # =============================================================

    def animar_morte(self):

        if self.modo != "morte":

            self.morte_timer.stop()

            return

        if not self.erro_morte:

            return

        self.morte_estado = not self.morte_estado

        if self.morte_estado:

            self.erro_morte.setStyleSheet("""
                QLabel {
                    color: #ff2222;
                    background-color: transparent;
                }
            """)

        else:

            self.erro_morte.setStyleSheet("""
                QLabel {
                    color: #550000;
                    background-color: transparent;
                }
            """)

    # =============================================================
    # TELA DE MORTE
    # =============================================================

    def tela_morte(self):

        self.modo = "morte"

        self.hud_timer.stop()

        self.timer.stop()

        self.limite_timer.stop()

        self.morte_timer.stop()

        # ---------------------------------------------------------
        # ESCONDER HUD
        # ---------------------------------------------------------

        self.titulo.hide()

        self.subtitulo.hide()

        self.status.hide()

        self.painel_timer.hide()

        self.estatisticas.hide()

        self.alerta.hide()

        self.instrucao.hide()

        self.credito.hide()

        for widget in self.findChildren(
            QFrame
        ):

            widget.hide()

        # ---------------------------------------------------------
        # LIMPAR OVERLAY ANTIGO
        # ---------------------------------------------------------

        if self.overlay_morte:

            self.overlay_morte.deleteLater()

            self.overlay_morte = None

        # ---------------------------------------------------------
        # OVERLAY
        # ---------------------------------------------------------

        self.overlay_morte = QWidget(
            self
        )

        self.overlay_morte.setGeometry(
            self.rect()
        )

        self.overlay_morte.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 175);
            }
        """)

        # ---------------------------------------------------------
        # TEXTO PRINCIPAL
        # ---------------------------------------------------------

        self.erro_morte = QLabel(
            "ERROR - VOCÊ MORREU ☠️",
            self.overlay_morte
        )

        self.erro_morte.setAlignment(
            Qt.AlignCenter
        )

        self.erro_morte.setFont(
            QFont(
                "Courier New",
                30,
                QFont.Bold
            )
        )

        self.erro_morte.setStyleSheet("""
            QLabel {
                color: #ff2222;
                background-color: transparent;
            }
        """)

        self.erro_morte.setGeometry(
            0,
            0,
            self.overlay_morte.width(),
            self.overlay_morte.height() - 60
        )

        # ---------------------------------------------------------
        # TENTAR NOVAMENTE
        # ---------------------------------------------------------

        self.retry_morte = QLabel(
            "Tentar novamente - Aperte Enter",
            self.overlay_morte
        )

        self.retry_morte.setAlignment(
            Qt.AlignCenter
        )

        self.retry_morte.setFont(
            QFont(
                "Courier New",
                13
            )
        )

        self.retry_morte.setStyleSheet("""
            QLabel {
                color: #bbbbbb;
                background-color: transparent;
            }
        """)

        self.retry_morte.setGeometry(
            0,
            self.overlay_morte.height() - 90,
            self.overlay_morte.width(),
            50
        )

        # ---------------------------------------------------------
        # MOSTRAR
        # ---------------------------------------------------------

        self.overlay_morte.raise_()

        self.erro_morte.show()

        self.retry_morte.show()

        self.overlay_morte.show()

        self.morte_estado = True

        self.morte_timer.start(
            500
        )

    # =============================================================
    # REINICIAR
    # =============================================================

    def reiniciar_jogo(self):

        self.morte_timer.stop()

        self.timer.stop()

        self.limite_timer.stop()

        # ---------------------------------------------------------
        # DESTRUIR TELA DE MORTE
        # ---------------------------------------------------------

        if self.overlay_morte:

            self.overlay_morte.hide()

            self.overlay_morte.deleteLater()

            self.overlay_morte = None

        self.erro_morte = None

        self.retry_morte = None

        # ---------------------------------------------------------
        # RESTAURAR HUD
        # ---------------------------------------------------------

        self.titulo.show()

        self.subtitulo.show()

        self.status.show()

        self.painel_timer.show()

        self.estatisticas.show()

        self.alerta.show()

        self.instrucao.show()

        self.credito.show()

        for widget in self.findChildren(
            QFrame
        ):

            widget.show()

        self.hud_timer.start(
            120
        )

        self.modo = "inicio"

        # ---------------------------------------------------------
        # ESTILO NORMAL
        # ---------------------------------------------------------

        self.setStyleSheet("""
            QWidget {
                background-color: #050505;
                color: #dddddd;
            }

            QFrame {
                background-color: #0b0b0b;
                border: 2px solid #333333;
                border-radius: 3px;
            }

            QLabel {
                color: #dddddd;
            }

            QProgressBar {
                background-color: #111111;
                border: 1px solid #444444;
                height: 9px;
            }

            QProgressBar::chunk {
                background-color: #00aa44;
            }
        """)

        self.mudar_cor(
            self.branco
        )

        self.titulo.setText(
            "RBMK-1000 // UNIDADE 4"
        )

        self.subtitulo.setText(
            "SISTEMA DE CONTROLE DO REATOR NUCLEAR"
        )

        self.status.setText(
            "● SISTEMA OFFLINE"
        )

        self.timer_label.setText(
            "00.00"
        )

        self.alvo.setText(
            "SISTEMA EM ESPERA"
        )

        self.alerta.setText(
            "SISTEMA PRONTO"
        )

        self.instrucao.setText(
            "PRESSIONE ENTER PARA INICIALIZAR"
        )

        self.flash_alerta.hide()