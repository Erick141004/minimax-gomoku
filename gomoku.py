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
    def __init__(self, tabuleiro=[Quadrado.V] * 100, turno=Quadrado.B):
        self.tabuleiro = tabuleiro  # estado do tabuleiro
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
        return self._venceu_linhas(self.tabuleiro) or self._venceu_colunas(self.tabuleiro) or self._venceu_diagonal(
            self.tabuleiro)

    def _venceu_linhas(self, tabuleiro):
        cor_atual = None
        tam_linha = int(np.sqrt(len(self.tabuleiro)))

        # verifica se cada linha contem 5 pecas da cor em questao
        for i in range(0, len(self.tabuleiro), tam_linha):
            cores_linha = 0
            for j in range(tam_linha):
                if tabuleiro[j + i] != Quadrado.V:
                    if cor_atual != tabuleiro[j + i]:
                        cor_atual = tabuleiro[j + i]
                        cores_linha = 1
                    elif cor_atual == tabuleiro[j + i]:
                        cores_linha += 1
                else:
                    cores_linha = 0

                if cores_linha == 5:
                    return True

        return False

    def _venceu_colunas(self, tabuleiro):
        cor_atual = None
        tam_linha = int(np.sqrt(len(self.tabuleiro)))

        # verifica se cada coluna contem 5 pecas da cor em questao
        for i in range(tam_linha):
            cores_coluna = 0
            for j in range(tam_linha):
                casa_atual = tabuleiro[i + (j * tam_linha)]
                if casa_atual != Quadrado.V:
                    if cor_atual != casa_atual:
                        cor_atual = casa_atual
                        cores_coluna = 1
                    elif cor_atual == casa_atual:
                        cores_coluna += 1
                else:
                    cores_coluna = 0

                if cores_coluna == 5:
                    return True

        return False

    def _venceu_diagonal(self, tabuleiro):
        venceu_cima_baixo = self.verifica_venceu_diagonal_cima_baixo(tabuleiro)
        venceu_baixo_cima = self.verifica_venceu_diagonal_baixo_cima(tabuleiro)

        return venceu_cima_baixo or venceu_baixo_cima

    def verifica_venceu_diagonal_cima_baixo(self, tabuleiro):
        cores_diagonal = 0
        cor_atual = None
        tam_linha = int(np.sqrt(len(self.tabuleiro)))
        for i in range(tam_linha):
            if tam_linha - i < 5:
                break

            if i == 0:
                desloca = 0
                for j in range(tam_linha):
                    casa_atual = tabuleiro[i + (j * tam_linha + desloca)]
                    if casa_atual != Quadrado.V:
                        if cor_atual != casa_atual:
                            cor_atual = casa_atual
                            cores_diagonal = 1
                        elif cor_atual == casa_atual:
                            cores_diagonal += 1
                    else:
                        cores_diagonal = 0

                    if cores_diagonal == 5:
                        return True

                    desloca += 1
            else:
                desloca_direita = 0
                for j in range(tam_linha - i):
                    casa_atual = tabuleiro[i + (j * tam_linha + desloca_direita)]
                    if casa_atual != Quadrado.V:
                        if cor_atual != casa_atual:
                            cor_atual = casa_atual
                            cores_diagonal = 1
                        elif cor_atual == casa_atual:
                            cores_diagonal += 1
                    else:
                        cores_diagonal = 0

                    if cores_diagonal == 5:
                        return True

                    desloca_direita += 1

                desloca_baixo = 0
                for j in range(tam_linha - i):
                    casa_atual = tabuleiro[i * tam_linha + (j * tam_linha + desloca_baixo)]
                    if casa_atual != Quadrado.V:
                        if cor_atual != casa_atual:
                            cor_atual = casa_atual
                            cores_diagonal = 1
                        elif cor_atual == casa_atual:
                            cores_diagonal += 1
                    else:
                        cores_diagonal = 0

                    if cores_diagonal == 5:
                        return True

                    desloca_baixo += 1

        return False

    def verifica_venceu_diagonal_baixo_cima(self, tabuleiro):
        cores_diagonal = 0
        cor_atual = None
        tam_linha = int(np.sqrt(len(self.tabuleiro)))

        for i in range(tam_linha):
            if tam_linha - i < 5:
                break

            if i == 0:
                desloca = 0
                for j in range(tam_linha):
                    casa_atual = tabuleiro[90 - (j * tam_linha - desloca)]
                    if casa_atual != Quadrado.V:
                        if cor_atual != casa_atual:
                            cor_atual = casa_atual
                            cores_diagonal = 1
                        elif cor_atual == casa_atual:
                            cores_diagonal += 1
                    else:
                        cores_diagonal = 0

                    if cores_diagonal == 5:
                        return True

                    desloca += 1
            else:
                desloca_direita = 0
                for j in range(tam_linha - i):
                    casa_atual = tabuleiro[90 + i - (j * tam_linha - desloca_direita)]
                    if casa_atual != Quadrado.V:
                        if cor_atual != casa_atual:
                            cor_atual = casa_atual
                            cores_diagonal = 1
                        elif cor_atual == casa_atual:
                            cores_diagonal += 1
                    else:
                        cores_diagonal = 0

                    if cores_diagonal == 5:
                        return True

                    desloca_direita += 1

                desloca_cima = 0
                for j in range(tam_linha - i):
                    casa_atual = tabuleiro[(90 - i * tam_linha) - (j * tam_linha - desloca_cima)]
                    if casa_atual != Quadrado.V:
                        if cor_atual != casa_atual:
                            cor_atual = casa_atual
                            cores_diagonal = 1
                        elif cor_atual == casa_atual:
                            cores_diagonal += 1
                    else:
                        cores_diagonal = 0

                    if cores_diagonal == 5:
                        return True

                    desloca_cima += 1

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
            if i % int(np.sqrt(len(self.tabuleiro))) != 0:
                tabuleiro_atual += f"""| {self.tabuleiro[i]} |"""
            else:
                tabuleiro_atual += f"""\n| {self.tabuleiro[i]} |"""

        return tabuleiro_atual
