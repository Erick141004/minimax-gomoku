import jogo_velha
import gomoku
from minimax import melhor_jogada_agente, melhor_jogada_agente_poda

if __name__ == "__main__":

    jogo = gomoku.Gomoku()

    def jogada_humano():
        jogada = -1
        while jogada not in jogo.jogos_validos():
            jogada = int(input("Escolha um quadrado (0-14):"))
        return jogada

    while True:
        humano = jogada_humano()
        jogo = jogo.jogar(humano)
        if jogo.venceu():
            print("Humano Venceu!")
            break
        elif jogo.empate():
            print("Empate!")
            break
        computador = melhor_jogada_agente_poda(jogo)
        # computador = jogada_humano()
        print(f"Jogada do Computador é {computador}")
        jogo = jogo.jogar(computador)
        print(jogo)
        if jogo.venceu():
            print("Computador venceu!")
            break
        elif jogo.empate():
            print("Empate!")
            break
