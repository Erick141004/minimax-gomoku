from gomoku import Gomoku, Quadrado
from minimax import melhor_jogada_agente, melhor_jogada_agente_poda, jogada_humano
from time import sleep

from q_learning import aprender, carregar_q_table, salvar_q_table

if __name__ == "__main__":

    jogo = Gomoku()
    # exibir_jogadas = "Jogadas = "
    primeira_jogada = True
    total_de_jogos = 0

    Gomoku.q_table = carregar_q_table()

    for x, y in Gomoku.q_table.items():
        print(f"Par: {x} | Valor: {y}")

    a = 1

    while total_de_jogos < 1000:
        while True:
            Gomoku.turno_atual = Quadrado.B
            humano = 0

            if primeira_jogada:
                humano = 112
                jogo = jogo.jogar(humano)
                primeira_jogada = False
                jogo.atualiza_pontos_observaveis(humano)
            else:
                # humano = melhor_jogada_agente(jogo, 2)
                # jogo = jogo.jogar(humano)
                jogo = aprender(jogo)

            Gomoku.tabuleiro_atual = jogo.tabuleiro

            # exibir_jogadas += f"⬜:{humano}, "

            if jogo.venceu():
                print(jogo)
                print("Humano Venceu!")
                break

            elif jogo.empate():
                print(jogo)
                print("Empate!")
                break

            # sleep(0.1)

            #computador = melhor_jogada_agente(jogo, 2)
            jogo = aprender(jogo)
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
                print("Computador venceu!")
                break

            elif jogo.empate():
                print(jogo)
                print("Empate!")
                break

        # sleep(1)
        salvar_q_table()

        Gomoku.pontos_observaveis = set()
        Gomoku.tabuleiro_atual = []
        Gomoku.turno_atual = Quadrado.V

        jogo = Gomoku()
        primeira_jogada = True

        total_de_jogos += 1
