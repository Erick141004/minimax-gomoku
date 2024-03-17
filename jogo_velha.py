from enum import Enum
from jogo import Jogo
from jogador import Jogador

class Quadrado(Jogador, Enum):
    X = "X"
    O = "O"
    V = " " # vazio

    def oposto(self):
        if self == Quadrado.X:
            return Quadrado.O
        elif self == Quadrado.O:
            return Quadrado.X
        else:
            return Quadrado.V

    def __str__(self):
        return self.value

class JogoVelha(Jogo):
    def __init__(self, posicao = [Quadrado.V] * 9, turno = Quadrado.X):
        self.posicao = posicao #estado tabuleiro
        self._turno = turno

    def turno(self):
        return self._turno
    
    def jogar(self, casa_jogada):
        temp = self.posicao.copy()
        temp[casa_jogada] = self._turno
        return JogoVelha(temp, self.turno().oposto())

    def jogos_validos(self):
        return [p for p in range(len(self.posicao)) if self.posicao[p] == Quadrado.V]
    
    def venceu(self):
        return self._venceu_linhas(self.posicao) or self._venceu_colunas(self.posicao) or self._venceu_diagonal(self.posicao) 

    def _venceu_linhas(self, posicao):
        return posicao[0] == posicao[1] and posicao[0] == posicao[2] and posicao[0] != Quadrado.V or \
        posicao[3] == posicao[4] and posicao[3] == posicao[5] and posicao[3] != Quadrado.V or \
        posicao[6] == posicao[7] and posicao[6] == posicao[8] and posicao[6] != Quadrado.V

    def _venceu_colunas(self, posicao):
        return posicao[0] == posicao[3] and posicao[0] == posicao[6] and posicao[0] != Quadrado.V or \
        posicao[1] == posicao[4] and posicao[1] == posicao[7] and posicao[1] != Quadrado.V or \
        posicao[2] == posicao[5] and posicao[2] == posicao[8] and posicao[2] != Quadrado.V

    def _venceu_diagonal(self, posicao):
        return posicao[0] == posicao[4] and posicao[0] == posicao[8] and posicao[0] != Quadrado.V or \
        posicao[2] == posicao[4] and posicao[2] == posicao[6] and posicao[2] != Quadrado.V

    def calcular_utilidade(self, jogador):
        if self.venceu() and self._turno == jogador:
            return -1
        elif self.venceu() and self._turno != jogador:
            return 1
        else:
            return 0

    def __str__(self):
        return f"""{self.posicao[0]}|{self.posicao[1]}|{self.posicao[2]}
-----
{self.posicao[3]}|{self.posicao[4]}|{self.posicao[5]}
-----
{self.posicao[6]}|{self.posicao[7]}|{self.posicao[8]}"""

