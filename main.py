from gomoku import Gomoku, Quadrado
from minimax import melhor_jogada_agente, melhor_jogada_agente_poda, jogada_humano
from time import sleep

from q_learning import aprender, carregar_q_table, salvar_q_table, jogar_melhor_recompensa

if __name__ == "__main__":

    partidas_ganhas_minimax = 0
    partidas_ganhas_q_learning = 0
    jogo = Gomoku()
    # exibir_jogadas = "Jogadas = "
    primeira_jogada = True
    id_do_jogo = 1
    total_de_jogos_limite = 1000  # QTD DE JOGOS PARA TREINAMENTO

    Gomoku.q_table = carregar_q_table()

    # for x, y in Gomoku.q_table.items():
    #     print(f"Par: {x} | Valor: {y}")
    #
    # a = 1

    while id_do_jogo <= total_de_jogos_limite:
        while True:
            Gomoku.turno_atual = Quadrado.B
            humano = 0

            if primeira_jogada:
                humano = 112
                jogo = jogo.jogar(humano)
                primeira_jogada = False
                jogo.atualiza_pontos_observaveis(humano)
            else:
                print(f"Antes dele jogar PO: {Gomoku.pontos_observaveis}")
                aprender(jogo)
                jogo, melhor_acao = jogar_melhor_recompensa(jogo)
                jogo.atualiza_pontos_observaveis(melhor_acao)
                print(f"Depois dele jogar PO: {Gomoku.pontos_observaveis}")

                #jogo = aprender(jogo)

            Gomoku.tabuleiro_atual = jogo.tabuleiro

            # exibir_jogadas += f"⬜:{humano}, "

            if jogo.venceu():
                print(jogo)
                print("Q-learning Venceu!")
                partidas_ganhas_minimax += 1
                break

            elif jogo.empate():
                print(jogo)
                print("Empate!")
                break

            # sleep(0.1)
            humano = melhor_jogada_agente(jogo, 2)
            jogo = jogo.jogar(humano)
            jogo.atualiza_pontos_observaveis(humano)
            #computador = melhor_jogada_agente(jogo, 2)


            # computador = melhor_jogada_agente_poda(jogo, 2)
            #jogo = jogo.jogar(computador)

            Gomoku.tabuleiro_atual = jogo.tabuleiro

            #jogo.atualiza_pontos_observaveis(computador)
            # print(f"Pontos observaveis: {jogo.pontos_observaveis}")
            # exibir_jogadas += f"⬛:{computador}, "
            # print(exibir_jogadas)

            print(jogo)
            if jogo.venceu():
                print(jogo)
                print("Minimax venceu!")
                partidas_ganhas_q_learning += 1
                break

            elif jogo.empate():
                print(jogo)
                print("Empate!")
                break

        # sleep(1)
        print(f"JOGO: {id_do_jogo} de {total_de_jogos_limite}.")
        salvar_q_table()

        # for x, y in Gomoku.q_table.items():
        #     if x[1] == 80 or x[1] == 95:
        #         print(f"Par: {x} | Valor: {y}")

        Gomoku.pontos_observaveis = set()
        Gomoku.tabuleiro_atual = []
        Gomoku.turno_atual = Quadrado.V

        jogo = Gomoku()
        primeira_jogada = True

        id_do_jogo += 1

    print(f"MINIMAX GANHOU {partidas_ganhas_minimax} PARTIDAS\nQ_LEARNING GANHOU {partidas_ganhas_q_learning} PARTIDAS")