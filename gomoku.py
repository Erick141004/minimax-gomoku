from enum import Enum
from jogador import Jogador
import numpy as np


class Quadrado(Jogador, Enum):
    # B = "B"  # branco
    B = "⬜"
    # P = "P"  # preto
    P = "⬛"
    # V = " "  # vazio
    V = "🟫"

    def oposto(self):
        if self == Quadrado.B:
            return Quadrado.P
        elif self == Quadrado.P:
            return Quadrado.B
        else:
            return Quadrado.V

    def __str__(self):
        return self.value


class Gomoku:

    pontos_observaveis = set()
    tabuleiro_atual = []
    turno_atual = Quadrado.V

    def __init__(
        self, tabuleiro: list[Quadrado] = [Quadrado.V] * 225, turno=Quadrado.B
    ):
        self.tabuleiro = tabuleiro  # estado do tabuleiro
        self._turno = turno

    def turno(self):
        return self._turno

    def jogar(self, ponto_jogado):
        novo_tabuleiro = self.tabuleiro.copy()
        novo_tabuleiro[ponto_jogado] = self._turno

        return Gomoku(novo_tabuleiro, self.turno().oposto())

    def jogos_validos(self):
        return [
            p for p in range(len(self.tabuleiro)) if self.tabuleiro[p] == Quadrado.V
        ]

    def regiao_jogada(self, pos):
        # canto superior esquerdo
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

    def verifica_ponto_jogavel(self, pontos_possiveis) -> set:
        pontos_nao_jogados = set()

        for ponto in pontos_possiveis:
            if self.tabuleiro[ponto] == Quadrado.V:
                pontos_nao_jogados.add(ponto)

        return pontos_nao_jogados

    def atualiza_pontos_observaveis(self, ponto_jogado):
        pontos_possiveis = self.retorna_pontos_possiveis(ponto_jogado)
        pontos_jogaveis = self.verifica_ponto_jogavel(pontos_possiveis)

        Gomoku.pontos_observaveis.update(pontos_jogaveis)

        if ponto_jogado in Gomoku.pontos_observaveis:
            Gomoku.pontos_observaveis.remove(ponto_jogado)

    def atualiza_pontos_observaveis_simulacao(
        self, pontos_observaveis_atual, ponto_jogado
    ):
        pontos_possiveis = self.retorna_pontos_possiveis(ponto_jogado)
        pontos_jogaveis = self.verifica_ponto_jogavel(pontos_possiveis)

        pontos_observaveis_atual.update(pontos_jogaveis)

        if ponto_jogado in pontos_observaveis_atual:
            pontos_observaveis_atual.remove(ponto_jogado)

    def retorna_pontos_possiveis(self, ponto_jogado):
        tam_linha = int(np.sqrt(len(self.tabuleiro)))
        pos_meio = ponto_jogado
        pontos_possiveis = None

        regiao_jogada = self.regiao_jogada(ponto_jogado)

        match (regiao_jogada):
            case 0:
                pontos_possiveis = [
                    pos_meio - tam_linha - 1,
                    pos_meio - tam_linha,
                    pos_meio - tam_linha + 1,
                    pos_meio - 1,
                    pos_meio + 1,
                    pos_meio + tam_linha - 1,
                    pos_meio + tam_linha,
                    pos_meio + tam_linha + 1,
                ]
            case 1:
                pontos_possiveis = [1, 15, 16]
            case 2:
                pontos_possiveis = [13, 28, 29]
            case 3:
                pontos_possiveis = [195, 196, 211]
            case 4:
                pontos_possiveis = [208, 209, 223]
            case 5:
                pontos_possiveis = [
                    pos_meio - 1,
                    pos_meio + 1,
                    pos_meio + tam_linha - 1,
                    pos_meio + tam_linha,
                    pos_meio + tam_linha + 1,
                ]
            case 6:
                pontos_possiveis = [
                    pos_meio - tam_linha - 1,
                    pos_meio - tam_linha,
                    pos_meio - tam_linha + 1,
                    pos_meio - 1,
                    pos_meio + 1,
                ]
            case 7:
                pontos_possiveis = [
                    pos_meio - tam_linha,
                    pos_meio - tam_linha + 1,
                    pos_meio + 1,
                    pos_meio + tam_linha,
                    pos_meio + tam_linha + 1,
                ]
            case 8:
                pontos_possiveis = [
                    pos_meio - tam_linha - 1,
                    pos_meio - tam_linha,
                    pos_meio - 1,
                    pos_meio + tam_linha - 1,
                    pos_meio + tam_linha,
                ]
        return pontos_possiveis

    def venceu(self):
        return (
            self._venceu_linhas(self.tabuleiro)
            or self._venceu_colunas(self.tabuleiro)
            or self._venceu_diagonal(self.tabuleiro)
        )

    def empate(self):
        return False

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
                    ponto_atual = tabuleiro[
                        i * tam_linha + (j * tam_linha + desloca_baixo)
                    ]
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
                    ponto_atual = tabuleiro[210 - (j * tam_linha - desloca)]
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
                    ponto_atual = tabuleiro[210 + i - (j * tam_linha - desloca_direita)]
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
                    ponto_atual = tabuleiro[
                        (210 - i * tam_linha) - (j * tam_linha - desloca_cima)
                    ]
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

    def estrela_linhas_pontos(self, origem, linha: list, jogador):
        tipo_seq = (
            -1
        )  # 0 = seq morta | 1 = talvez valida | 2 = valida (origem faz parte da seq)  # noqa: E501
        pontos = 0

        print(self)

        if origem == 114:
            abc = 1

        if jogador == Gomoku.turno_atual:
            tipo_seq = 2
        elif jogador == Gomoku.turno_atual.oposto():
            tipo_seq = 1

        for casa in linha:
            if casa in range(len(self.tabuleiro)):
                if jogador == Gomoku.turno_atual:
                    if self.tabuleiro[casa] == jogador.oposto():  # HUMANO
                        tipo_seq = 0
                        pontos = 0
                    elif self.tabuleiro[casa] == Quadrado.V:
                        pontos += 0
                    else:
                        if tipo_seq == 0:
                            tipo_seq = 1
                            pontos = 1
                            distancia_origem_casa = abs(
                                linha.index(casa) - linha.index(origem)
                            )  # noqa: E501
                            if (
                                distancia_origem_casa < 2
                            ):  # significa que sao vizinhas ou eh a casa atual  # noqa: E501
                                tipo_seq = 2
                        elif tipo_seq == 1:
                            pontos += 1
                            distancia_origem_casa = abs(
                                linha.index(casa) - linha.index(origem)
                            )  # noqa: E501
                            if (
                                distancia_origem_casa < 2
                            ):  # significa que sao vizinhas ou eh a casa atual  # noqa: E501
                                tipo_seq = 2
                        elif tipo_seq == 2:
                            pontos += 1
               elif jogador == Gomoku.turno_atual.oposto():
                    if self.tabuleiro[casa] == jogador.oposto():  # AGENTE
                        if (linha[linha.index(origem)] == linha[linha.index(casa)]):  # noqa: E501
                            tipo_seq = 2
                            pontos += 0
                        elif tipo_seq == 2:
                            break
                        else:
                            tipo_seq = 0
                            pontos = 0
                    elif self.tabuleiro[casa] == Quadrado.V:
                        pontos -= 1
                    else:
                        if tipo_seq == 0:
                            tipo_seq = 1
                            pontos = 1
                        elif tipo_seq == 1:
                            pontos += 1
                        elif tipo_seq == 2:
                            pontos += 1

        if tipo_seq == 2:
            return pontos
        else:
            return 0

    def calcula_estrela(self, proximo_jogo, jogador):

        tam_linha = int(np.sqrt(len(self.tabuleiro)))
        vertical = horizontal = diagonal_sl = diagonal_nl = None

        origem = proximo_jogo

        vertical = [
            self.valida_casa_linha(origem, origem - (tam_linha * 4), 4),
            self.valida_casa_linha(origem, origem - (tam_linha * 3), 3),
            self.valida_casa_linha(origem, origem - (tam_linha * 2), 2),
            self.valida_casa_linha(origem, origem - tam_linha, 1),
            origem,
            self.valida_casa_linha(origem, origem + tam_linha, 1),
            self.valida_casa_linha(origem, origem + (tam_linha * 2), 2),
            self.valida_casa_linha(origem, origem + (tam_linha * 3), 3),
            self.valida_casa_linha(origem, origem + (tam_linha * 4), 4),
        ]

        horizontal = [
            self.valida_casa_linha(origem, origem - 4, 0),
            self.valida_casa_linha(origem, origem - 3, 0),
            self.valida_casa_linha(origem, origem - 2, 0),
            self.valida_casa_linha(origem, origem - 1, 0),
            origem,
            self.valida_casa_linha(origem, origem + 1, 0),
            self.valida_casa_linha(origem, origem + 2, 0),
            self.valida_casa_linha(origem, origem + 3, 0),
            self.valida_casa_linha(origem, origem + 4, 0),
        ]

        diagonal_sl = [
            self.valida_casa_linha(origem, origem - (tam_linha * 4) - 4, 4),
            self.valida_casa_linha(origem, origem - (tam_linha * 3) - 3, 3),
            self.valida_casa_linha(origem, origem - (tam_linha * 2) - 2, 2),
            self.valida_casa_linha(origem, origem - tam_linha - 1, 1),
            origem,
            self.valida_casa_linha(origem, origem + tam_linha + 1, 1),
            self.valida_casa_linha(origem, origem + (tam_linha * 2) + 2, 2),
            self.valida_casa_linha(origem, origem + (tam_linha * 3) + 3, 3),
            self.valida_casa_linha(origem, origem + (tam_linha * 4) + 4, 4),
        ]

        diagonal_nl = [
            self.valida_casa_linha(origem, origem + (tam_linha * 4) - 4, 4),
            self.valida_casa_linha(origem, origem + (tam_linha * 3) - 3, 3),
            self.valida_casa_linha(origem, origem + (tam_linha * 2) - 2, 2),
            self.valida_casa_linha(origem, origem + tam_linha - 1, 1),
            origem,
            self.valida_casa_linha(origem, origem - tam_linha + 1, 1),
            self.valida_casa_linha(origem, origem - (tam_linha * 2) + 2, 2),
            self.valida_casa_linha(origem, origem - (tam_linha * 3) + 3, 3),
            self.valida_casa_linha(origem, origem - (tam_linha * 4) + 4, 4),
        ]

        vertical_valor = self.estrela_linhas_pontos(origem, vertical, jogador)
        horizontal_valor = self.estrela_linhas_pontos(origem, horizontal, jogador)
        diagonal_sl_valor = self.estrela_linhas_pontos(origem, diagonal_sl, jogador)
        diagonal_nl_valor = self.estrela_linhas_pontos(origem, diagonal_nl, jogador)

        tuplas = [
            (vertical_valor, vertical),
            (horizontal_valor, horizontal),
            (diagonal_sl_valor, diagonal_sl),
            (diagonal_nl_valor, diagonal_nl),
        ]

        return max(tuplas)

    def valida_casa_linha(self, origem, ponto, distancia):
        linha_origem = origem // 15
        linha_ponto = ponto // 15

        if abs(linha_ponto - linha_origem) != distancia:
            return -1
        else:
            return ponto

    def calcular_utilidade(self, jogador, proximo_jogo):
        if self.venceu() and self._turno == jogador:
            print(f"O AGENTE VAI GANHAR NESSE MOMENTO {jogador}")
            print(self)
            return float("-inf")
        elif self.venceu() and self._turno != jogador:
            print(f"O AGENTE VAI PERDER NESSE MOMENTO {jogador}")
            print(self)
            return float("inf")
        else:
            return self.calcula_diferenca_peso(proximo_jogo)

    def calcula_diferenca_peso(self, proximo_jogo):
        linha_melhor_agente = self.calcula_estrela(proximo_jogo, Gomoku.turno_atual)
        linha_melhor_humano = self.calcula_estrela(
            proximo_jogo, Gomoku.turno_atual.oposto()
        )

        if linha_melhor_agente[0] <= linha_melhor_humano[0]:
            return (linha_melhor_humano[0] * 10) + 1
        else:
            return linha_melhor_agente[0] * 10

    def regiao_humano(self):
        self.pos_anteriores = set()
        pos_inimigo = np.where(self.tabuleiro == "B")

        if pos_inimigo is not self.pos_anteriores:
            self.pos_anteriores.update(pos_inimigo)

    def __str__(self):
        tabuleiro_atual = ""
        for i in range(len(self.tabuleiro)):
            if i % int(np.sqrt(len(self.tabuleiro))) != 0:
                # tabuleiro_atual += f"""| {self.tabuleiro[i]} ({str(i).zfill(3)}) |"""
                tabuleiro_atual += f"""{self.tabuleiro[i]}{str(i).zfill(3)}"""
            else:
                # tabuleiro_atual += f"""\n| {self.tabuleiro[i]} ({str(i).zfill(3)}) |"""
                tabuleiro_atual += f"""\n\n{self.tabuleiro[i]}{str(i).zfill(3)}"""

        return tabuleiro_atual
