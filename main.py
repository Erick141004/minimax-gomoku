import jogo_velha
import gomoku
from minimax import melhor_jogada_agente, melhor_jogada_agente_poda

if __name__ == "__main__":

    jogo = gomoku.Gomoku()

    def jogada_humano():
        jogada = -1
        while jogada not in jogo.jogos_validos():
            jogada = int(input("Escolha um quadrado (0-224):"))
        return jogada

    while True:
        humano = jogada_humano()
        jogo = jogo.jogar(humano)

        gomoku.Gomoku.tabuleiro_atual = jogo.tabuleiro

        jogo.atualiza_pontos_observaveis(humano)

        print(f"Pontos observaveis: {jogo.pontos_observaveis}")

        if jogo.venceu():
            print(jogo)
            print("Humano Venceu!")
            break
        elif jogo.empate():
            print(jogo)
            print("Empate!")
            break

        computador = melhor_jogada_agente_poda(jogo, 8)
        # computador = jogada_humano()
        print(f"Jogada do Computador é {computador}")
        jogo = jogo.jogar(computador)
        gomoku.Gomoku.tabuleiro_atual = jogo.tabuleiro

        jogo.atualiza_pontos_observaveis(computador)
        print(f"Pontos observaveis: {jogo.pontos_observaveis}")

        print(jogo)
        if jogo.venceu():
            print(jogo)
            print("Computador venceu!")
            break
        elif jogo.empate():
            print(jogo)
            print("Empate!")
            break
