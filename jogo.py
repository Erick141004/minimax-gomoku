from gomoku import Quadrado


class Jogo():
    def turno(self):
        pass

    def jogar(self, localizacao):
        localizacao.faz_nada
        pass

    def jogos_validos(self):
        return [Quadrado.V]

    def venceu(self):
        pass

    def empate(self):
        return (not self.venceu()) and (len(self.jogos_validos()) == 0)

    def avaliar(self, player):
        player.faz_nada
        pass
