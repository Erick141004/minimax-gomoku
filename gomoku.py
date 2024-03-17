from enum import Enum
from jogo import Jogo
from jogador import Jogador
import numpy as np

class Quadrado(Jogador, Enum):
    B = "B"  # branco
    P = "P"  # preto
    V = " "  # vazio

    def oposto(self):
        if self == Quadrado.B:
            return Quadrado.P
        elif self == Quadrado.P:
            return Quadrado.B
        else:
            return Quadrado.V

    def __str__(self):
        return self.value

class Gomoku(Jogo):
    def __init__(self, tabuleiro = [Quadrado.V] * 9, turno = Quadrado.B):
        self.tabuleiro = tabuleiro  #estado do tabuleiro
        self._turno = turno

    def turno(self):
        return self._turno
    
    def jogar(self, casa_jogada):
        temp = self.tabuleiro.copy()
        temp[casa_jogada] = self._turno
        return Gomoku(temp, self.turno().oposto())

    def jogos_validos(self):
        return [p for p in range(len(self.tabuleiro)) if self.tabuleiro[p] == Quadrado.V]
    
    def venceu(self):
        return self._venceu_linhas(self.tabuleiro) or self._venceu_colunas(self.tabuleiro) or self._venceu_diagonal(self.tabuleiro)

    def _venceu_linhas(self, tabuleiro):

        cores_linha = 0
        cor_atual = None
        tam_linha = int(np.sqrt(len(self.tabuleiro)))

        # verifica se cada linha contem 5 pecas da cor em questao
        for i in range(0, len(self.tabuleiro), tam_linha):
            for j in range(tam_linha):
                if tabuleiro[j + i] != Quadrado.V:
                    if cor_atual != tabuleiro[j + i]:
                        cor_atual = tabuleiro[j + i]
                        cores_linha = 1
                    elif cor_atual == tabuleiro[j + i]:
                        cores_linha += 1

                    if cores_linha == 3:
                        return True

        return False

    def _venceu_colunas(self, tabuleiro):
        cores_coluna = 0
        cor_atual = None
        tam_linha = int(np.sqrt(len(self.tabuleiro)))

        # verifica se cada coluna contem 5 pecas da cor em questao
        for i in range(0, tam_linha):
            for j in range(tam_linha):
                if tabuleiro[i + (j * tam_linha)] != Quadrado.V:
                    if cor_atual != tabuleiro[i + (j * tam_linha)]:
                        cor_atual = tabuleiro[i + (j * tam_linha)]
                        cores_coluna = 1
                    elif cor_atual == tabuleiro[i + (j * tam_linha)]:
                        cores_coluna += 1

                    if cores_coluna == 3:
                        return True

        return False

    def _venceu_diagonal(self, tabuleiro):
        return False

    def calcular_utilidade(self, jogador):
        if self.venceu() and self._turno == jogador:
            return -1
        elif self.venceu() and self._turno != jogador:
            return 1
        else:
            return 0

    def __str__(self):
        tabuleiro_atual = ""
        for i in range(len(self.tabuleiro)):
            if i % 3 != 0:
                tabuleiro_atual += f"""| {self.tabuleiro[i]} |"""
            else:
                tabuleiro_atual += f"""\n| {self.tabuleiro[i]} |"""

        return tabuleiro_atual


