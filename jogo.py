import random
import time


class Jogo:

    def __init__(self):
        self.tempo_alvo = 0
        self.tempo_inicio = 0
        self.rodando = False

    def novo_desafio(self):

        self.tempo_alvo = random.choice([
            2.0,
            2.5,
            3.0,
            3.5,
            4.0,
            4.5,
            5.0
        ])

        self.tempo_inicio = 0
        self.rodando = False

    def iniciar(self):

        self.tempo_inicio = time.perf_counter()
        self.rodando = True

    def parar(self):

        if not self.rodando:
            return None

        tempo_final = time.perf_counter()

        tempo_decorrido = (
            tempo_final - self.tempo_inicio
        )

        self.rodando = False

        diferenca = abs(
            tempo_decorrido - self.tempo_alvo
        )

        return {
            "tempo_alvo": self.tempo_alvo,
            "tempo_jogador": tempo_decorrido,
            "diferenca": diferenca,
            "acertou": diferenca <= 0.15
        }