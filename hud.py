from PySide6.QtWidgets import QWidget, QFrame
from PySide6.QtCore import QTimer


class HUD:

    def __init__(self, interface):

        self.interface = interface

        self.estado_pisca = False

        self.timer_pisca = QTimer()

        self.timer_pisca.timeout.connect(
            self.piscar_indicadores
        )

        self.timer_pisca.start(400)

    # =========================================================
    # PISCAR INDICADORES
    # =========================================================

    def piscar_indicadores(self):

        if self.interface.modo not in (
            "jogando",
            "pronto"
        ):
            return

        self.estado_pisca = not self.estado_pisca

        if self.estado_pisca:

            self.interface.indicador_core.setStyleSheet(
                "color: #00ff66;"
            )

            self.interface.indicador_cooling.setStyleSheet(
                "color: #00ff66;"
            )

            self.interface.indicador_control.setStyleSheet(
                "color: #00ff66;"
            )

        else:

            self.interface.indicador_core.setStyleSheet(
                "color: #006633;"
            )

            self.interface.indicador_cooling.setStyleSheet(
                "color: #006633;"
            )

            self.interface.indicador_control.setStyleSheet(
                "color: #006633;"
            )

    # =========================================================
    # ESTILO DOS PAINÉIS
    # =========================================================

    def aplicar_paineis(self):

        for widget in self.interface.findChildren(QFrame):

            widget.setStyleSheet("""
                QFrame {
                    background-color: #080808;
                    border: 2px solid #292929;
                    border-radius: 2px;
                }
            """)

    # =========================================================
    # TIMER
    # =========================================================

    def destacar_timer(self, cor):

        self.interface.timer_label.setStyleSheet(
            f"""
            QLabel {{
                color: {cor};
                background-color: #050505;
                border: 3px solid {cor};
                padding: 15px;
            }}
            """
        )

    # =========================================================
    # ALERTA
    # =========================================================

    def destacar_alerta(self, cor):

        self.interface.alerta.setStyleSheet(
            f"""
            QLabel {{
                color: {cor};
                border: 2px solid {cor};
                padding: 8px;
            }}
            """
        )