from gomoku import Gomoku, Quadrado
from minimax import melhor_jogada_agente, melhor_jogada_agente_poda, jogada_humano
from time import sleep

from q_learning import aprender, carregar_q_table, salvar_q_table


if __name__ == "__main__":

    jogo = Gomoku()
    exibir_jogadas = "Jogadas = "
    primeira_jogada = True

    # Gomoku.q_table = carregar_q_table()

    while True:
        # humano = jogada_humano()
        Gomoku.turno_atual = Quadrado.B
        humano = 0

        if primeira_jogada:
            humano = 2
            jogo = jogo.jogar(humano)
            primeira_jogada = False
        else:
            humano = melhor_jogada_agente(jogo, 2)
            jogo = jogo.jogar(humano)

        Gomoku.tabuleiro_atual = jogo.tabuleiro

        jogo.atualiza_pontos_observaveis(humano)

        # exibir_jogadas += f"⬜:{humano}, "

        if jogo.venceu():
            print(jogo)
            print("Humano Venceu!")
            jogo.blabla(jogo.tabuleiro)
            break
        elif jogo.empate():
            print(jogo)
            print("Empate!")
            break

        # sleep(0.1)

        computador = melhor_jogada_agente(jogo, 2)
        # computador2, utilidade2 = aprender(jogo)
        # computador = melhor_jogada_agente_poda(jogo, 2)
        # computador = jogada_humano()
        jogo = jogo.jogar(computador)
        Gomoku.tabuleiro_atual = jogo.tabuleiro

        jogo.atualiza_pontos_observaveis(computador)
        # print(f"Pontos observaveis: {jogo.pontos_observaveis}")
        # exibir_jogadas += f"⬛:{computador}, "
        # print(exibir_jogadas)

        print(jogo)
        if jogo.venceu():
            print(jogo)
            print("Computador venceu!")
            break
        elif jogo.empate():
            print(jogo)
            print("Empate!")
            break

    salvar_q_table()
