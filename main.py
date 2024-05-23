from gomoku import Gomoku, Quadrado
from minimax import melhor_jogada_agente, melhor_jogada_agente_poda

if __name__ == "__main__":

    jogo = Gomoku()
    exibir_jogadas = "Jogadas = "

    def jogada_humano():
        Gomoku.turno_atual = Quadrado.B
        jogada = -1
        while jogada not in jogo.jogos_validos():
            jogada = int(input("Escolha um quadrado (0-224):"))
        return jogada

    while True:
        humano = jogada_humano()
        jogo = jogo.jogar(humano)

        Gomoku.tabuleiro_atual = jogo.tabuleiro

        jogo.atualiza_pontos_observaveis(humano)

        print(f"Pontos observaveis: {jogo.pontos_observaveis}")
        exibir_jogadas += f"⬜:{humano}, "
        print(exibir_jogadas)

        if jogo.venceu():
            print(jogo)
            print("Humano Venceu!")
            break
        elif jogo.empate():
            print(jogo)
            print("Empate!")
            break

        # computador = melhor_jogada_agente(jogo, 2)
        computador = melhor_jogada_agente_poda(jogo, 2)
        # computador = jogada_humano()
        print(f"Jogada do Computador é {computador}")
        jogo = jogo.jogar(computador)
        Gomoku.tabuleiro_atual = jogo.tabuleiro

        jogo.atualiza_pontos_observaveis(computador)
        print(f"Pontos observaveis: {jogo.pontos_observaveis}")
        exibir_jogadas += f"⬛:{computador}, "
        print(exibir_jogadas)

        print(jogo)
        if jogo.venceu():
            print(jogo)
            print("Computador venceu!")
            break
        elif jogo.empate():
            print(jogo)
            print("Empate!")
            break
