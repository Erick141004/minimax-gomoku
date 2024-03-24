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

    pontos_observaveis = set()

    def __init__(self, tabuleiro=[Quadrado.V] * 225, turno=Quadrado.B):
        self.tabuleiro = tabuleiro  # estado do tabuleiro
        self._turno = turno

    def turno(self):
        return self._turno

    def jogar(self, ponto_jogado):
        temp = self.tabuleiro.copy()
        temp[ponto_jogado] = self._turno

        return Gomoku(temp, self.turno().oposto())

    def jogos_validos(self):
        return [p for p in range(len(self.tabuleiro)) if self.tabuleiro[p] == Quadrado.V]

    def regiao_jogada(self, pos):
        #canto superior esquerdo
        if pos == 0:
            return 1
        # canto superior direito
        elif pos == 14:
            return 2
        # canto inferior esquerdo
        elif pos == 210:
            return 3
        # canto inferior direito
        elif pos == 224:
            return 4
        # linha superior sem os cantos
        elif pos in range(1, 14):
            return 5
        # linha inferior sem os cantos
        elif pos in range(211, 224):
            return 6
        # coluna esquerda sem os cantos
        elif pos in range(15, 210, 15):
            return 7
        # coluna direita sem os cantos
        elif pos in range(29, 224, 15):
            return 8
        # senao, esta no meio
        else:
            return 0

    def verifica_ponto_jogavel(self, pontos_possiveis):
        pontos_nao_jogados = []

        for ponto in pontos_possiveis:
           if self.tabuleiro[ponto] == Quadrado.V:
               pontos_nao_jogados.append(ponto)

        return pontos_nao_jogados

    def atualiza_pontos_observaveis(self, ponto_jogado):
        tam_linha = int(np.sqrt(len(self.tabuleiro)))
        pos_meio = ponto_jogado
        pontos_possiveis = None

        regiao_jogada = self.regiao_jogada(ponto_jogado)

        match(regiao_jogada):
            case 0:
                pontos_possiveis = [pos_meio - tam_linha - 1,
                                    pos_meio - tam_linha,
                                    pos_meio - tam_linha + 1,
                                    pos_meio - 1,
                                    pos_meio + 1,
                                    pos_meio + tam_linha - 1,
                                    pos_meio + tam_linha,
                                    pos_meio + tam_linha + 1]
            case 1:
                pontos_possiveis = [1, 15, 16]
            case 2:
                pontos_possiveis = [13, 28, 29]
            case 3:
                pontos_possiveis = [195, 196, 211]
            case 4:
                pontos_possiveis = [208, 209, 223]
            case 5:
                pontos_possiveis = [pos_meio - 1,
                                    pos_meio + 1,
                                    pos_meio + tam_linha - 1,
                                    pos_meio + tam_linha,
                                    pos_meio + tam_linha + 1]
            case 6:
                pontos_possiveis = [pos_meio - tam_linha - 1,
                                    pos_meio - tam_linha,
                                    pos_meio - tam_linha + 1,
                                    pos_meio - 1,
                                    pos_meio + 1]
            case 7:
                pontos_possiveis = [pos_meio - tam_linha,
                                    pos_meio - tam_linha + 1,
                                    pos_meio + 1,
                                    pos_meio + tam_linha,
                                    pos_meio + tam_linha + 1]
            case 8:
                pontos_possiveis = [pos_meio - tam_linha - 1,
                                    pos_meio - tam_linha,
                                    pos_meio - 1,
                                    pos_meio + tam_linha - 1,
                                    pos_meio + tam_linha]

        pontos_possiveis = self.verifica_ponto_jogavel(pontos_possiveis)

        Gomoku.pontos_observaveis.update(pontos_possiveis)

        if ponto_jogado in Gomoku.pontos_observaveis:
            Gomoku.pontos_observaveis.remove(ponto_jogado)

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
                ponto_atual = tabuleiro[i + (j * tam_linha)]
                if ponto_atual != Quadrado.V:
                    if cor_atual != ponto_atual:
                        cor_atual = ponto_atual
                        cores_coluna = 1
                    elif cor_atual == ponto_atual:
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
                    ponto_atual = tabuleiro[i + (j * tam_linha + desloca)]
                    if ponto_atual != Quadrado.V:
                        if cor_atual != ponto_atual:
                            cor_atual = ponto_atual
                            cores_diagonal = 1
                        elif cor_atual == ponto_atual:
                            cores_diagonal += 1
                    else:
                        cores_diagonal = 0

                    if cores_diagonal == 5:
                        return True

                    desloca += 1
            else:
                desloca_direita = 0
                for j in range(tam_linha - i):
                    ponto_atual = tabuleiro[i + (j * tam_linha + desloca_direita)]
                    if ponto_atual != Quadrado.V:
                        if cor_atual != ponto_atual:
                            cor_atual = ponto_atual
                            cores_diagonal = 1
                        elif cor_atual == ponto_atual:
                            cores_diagonal += 1
                    else:
                        cores_diagonal = 0

                    if cores_diagonal == 5:
                        return True

                    desloca_direita += 1

                desloca_baixo = 0
                for j in range(tam_linha - i):
                    ponto_atual = tabuleiro[i * tam_linha + (j * tam_linha + desloca_baixo)]
                    if ponto_atual != Quadrado.V:
                        if cor_atual != ponto_atual:
                            cor_atual = ponto_atual
                            cores_diagonal = 1
                        elif cor_atual == ponto_atual:
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
                    ponto_atual = tabuleiro[90 - (j * tam_linha - desloca)]
                    if ponto_atual != Quadrado.V:
                        if cor_atual != ponto_atual:
                            cor_atual = ponto_atual
                            cores_diagonal = 1
                        elif cor_atual == ponto_atual:
                            cores_diagonal += 1
                    else:
                        cores_diagonal = 0

                    if cores_diagonal == 5:
                        return True

                    desloca += 1
            else:
                desloca_direita = 0
                for j in range(tam_linha - i):
                    ponto_atual = tabuleiro[90 + i - (j * tam_linha - desloca_direita)]
                    if ponto_atual != Quadrado.V:
                        if cor_atual != ponto_atual:
                            cor_atual = ponto_atual
                            cores_diagonal = 1
                        elif cor_atual == ponto_atual:
                            cores_diagonal += 1
                    else:
                        cores_diagonal = 0

                    if cores_diagonal == 5:
                        return True

                    desloca_direita += 1

                desloca_cima = 0
                for j in range(tam_linha - i):
                    ponto_atual = tabuleiro[(90 - i * tam_linha) - (j * tam_linha - desloca_cima)]
                    if ponto_atual != Quadrado.V:
                        if cor_atual != ponto_atual:
                            cor_atual = ponto_atual
                            cores_diagonal = 1
                        elif cor_atual == ponto_atual:
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

    def regiao_humano(self):
        self.pos_anteriores = set()
        pos_inimigo = np.where(self.tabuleiro == "B")

        if pos_inimigo is not self.pos_anteriores:
            self.pos_anteriores.update(pos_inimigo)

    def __str__(self):
        tabuleiro_atual = ""
        for i in range(len(self.tabuleiro)):
            if i % int(np.sqrt(len(self.tabuleiro))) != 0:
                tabuleiro_atual += f"""| {self.tabuleiro[i]} ({str(i).zfill(3)}) |"""
            else:
                tabuleiro_atual += f"""\n| {self.tabuleiro[i]} ({str(i).zfill(3)}) |"""

        return tabuleiro_atual
