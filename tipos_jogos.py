from gomoku import Gomoku, Quadrado
from minimax import melhor_jogada_agente
from q_learning import (
    aprender,
    carregar_q_table,
    estado_na_lista,
    jogar_aleatorio_recompensa,
    jogar_melhor_recompensa,
    salvar_q_table,
)


def verifica_venceu(jogo):
    if jogo.venceu():
        print(jogo)
        print(f"{Gomoku.turno_atual} venceu!")
        return True
    elif jogo.empate():
        print(jogo)
        print("Empate!")
        return True

    return False


def reseta_tabuleiro():
    Gomoku.pontos_observaveis = set()
    Gomoku.tabuleiro_atual = []
    Gomoku.turno_atual = Quadrado.V
    Gomoku.historico_jogadas = []


def humano_vs_humano():
    Gomoku.ia_vs_ia = False
    jogo = Gomoku()

    while True:
        jogada = jogo.jogada_humano()
        jogo = jogo.jogar(jogada)

        jogo.adiciona_historico_jogada(jogada)
        jogo.printa_historico_jogada()
        print(jogo)

        if verifica_venceu(jogo):
            break

        jogada = jogo.jogada_humano()
        jogo = jogo.jogar(jogada)

        jogo.adiciona_historico_jogada(jogada)
        jogo.printa_historico_jogada()
        print(jogo)

        if verifica_venceu(jogo):
            break

    jogo.limpa_historico_jogada()


def humano_vs_minimax():
    Gomoku.ia_vs_ia = False
    jogo = Gomoku()

    while True:
        jogada = jogo.jogada_humano()
        jogo = jogo.jogar(jogada)

        jogo.adiciona_historico_jogada(jogada)
        jogo.printa_historico_jogada()
        jogo.atualiza_pontos_observaveis(jogada)
        jogo.atualiza_tabuleiro()
        print(jogo)

        if verifica_venceu(jogo):
            break

        jogada = melhor_jogada_agente(jogo, 2)
        jogo = jogo.jogar(jogada)

        jogo.adiciona_historico_jogada(jogada)
        jogo.printa_historico_jogada()
        jogo.atualiza_pontos_observaveis(jogada)
        jogo.atualiza_tabuleiro()
        print(jogo)

        if verifica_venceu(jogo):
            break

    jogo.limpa_historico_jogada()


def humano_vs_qlearning():
    Gomoku.ia_vs_ia = False

    Gomoku.alpha = 0.2
    Gomoku.gamma = 0.8
    Gomoku.epsilon = 0.2

    carregar_q_table()
    jogo = Gomoku()

    while True:
        jogada = jogo.jogada_humano()
        jogo = jogo.jogar(jogada)

        jogo.adiciona_historico_jogada(jogada)
        jogo.printa_historico_jogada()
        jogo.atualiza_pontos_observaveis(jogada)
        jogo.atualiza_tabuleiro()
        print(jogo)

        if verifica_venceu(jogo):
            break

        jogo.define_ou_inverte_jogador_atual()
        aprender(jogo)
        jogo, melhor_acao = jogar_melhor_recompensa(jogo)

        jogo.adiciona_historico_jogada(melhor_acao)
        jogo.printa_historico_jogada()
        jogo.atualiza_pontos_observaveis(melhor_acao)
        jogo.atualiza_tabuleiro()
        print(jogo)

        if verifica_venceu(jogo):
            break

    jogo.limpa_historico_jogada()
    salvar_q_table()


def humano_vs_minimax_qlearning():
    Gomoku.ia_vs_ia = False

    Gomoku.alpha = 0.2
    Gomoku.gamma = 0.8
    Gomoku.epsilon = 0.2

    carregar_q_table()
    jogo = Gomoku()

    while True:
        jogada = jogo.jogada_humano()
        jogo = jogo.jogar(jogada)

        jogo.adiciona_historico_jogada(jogada)
        jogo.printa_historico_jogada()
        jogo.atualiza_pontos_observaveis(jogada)
        jogo.atualiza_tabuleiro()
        print(jogo)

        if verifica_venceu(jogo):
            break

        if estado_na_lista(jogo):
            jogo.define_ou_inverte_jogador_atual()
            aprender(jogo)
            jogo, jogada = jogar_melhor_recompensa(jogo)
            jogo.atualiza_pontos_observaveis(jogada)
            print("QLearning")
        else:
            jogada = melhor_jogada_agente(jogo, 2)
            aprender(jogo)
            jogo = jogo.jogar(jogada)
            jogo.atualiza_pontos_observaveis(jogada)
            print("Minimax")

        jogo.adiciona_historico_jogada(jogada)
        jogo.printa_historico_jogada()
        jogo.atualiza_pontos_observaveis(jogada)
        jogo.atualiza_tabuleiro()
        print(jogo)

        if verifica_venceu(jogo):
            break

    jogo.limpa_historico_jogada()
    salvar_q_table()


def qlearning_vs_minimax():
    Gomoku.ia_vs_ia = True

    Gomoku.alpha = 0.2
    Gomoku.gamma = 0.8
    Gomoku.epsilon = 0.2

    carregar_q_table()
    jogo = Gomoku()

    primeira_jogada = True

    while True:
        if primeira_jogada:
            melhor_acao = 112
            jogo = jogo.jogar(melhor_acao)
            primeira_jogada = False
            jogo.adiciona_historico_jogada(melhor_acao)
            jogo.printa_historico_jogada()
            jogo.atualiza_pontos_observaveis(melhor_acao)
            jogo.atualiza_tabuleiro()
            print(jogo)
        else:
            jogo.define_ou_inverte_jogador_atual()
            aprender(jogo)
            jogo, melhor_acao = jogar_melhor_recompensa(jogo)
            jogo.adiciona_historico_jogada(melhor_acao)
            jogo.printa_historico_jogada()
            jogo.atualiza_pontos_observaveis(melhor_acao)
            jogo.atualiza_tabuleiro()
            print(jogo)

        if verifica_venceu(jogo):
            break

        jogada = melhor_jogada_agente(jogo, 2)
        jogo = jogo.jogar(jogada)

        jogo.adiciona_historico_jogada(jogada)
        jogo.printa_historico_jogada()
        jogo.atualiza_pontos_observaveis(jogada)
        jogo.atualiza_tabuleiro()
        print(jogo)

        if verifica_venceu(jogo):
            break

    jogo.limpa_historico_jogada()
    salvar_q_table()


def treino_qlearning_vs_minimax(quantidade):
    Gomoku.ia_vs_ia = True

    Gomoku.alpha = 0.7
    Gomoku.gamma = 0.3
    Gomoku.epsilon = 0.8

    carregar_q_table()
    jogo = Gomoku()

    primeira_jogada = True

    numero_treino = 1
    qntd_vitorias_qlearning = 0
    qntd_vitorias_minimax = 0

    while True:
        if primeira_jogada:
            jogo = Gomoku()
            jogo.define_ou_inverte_jogador_atual()
            melhor_acao = 112
            jogo = jogo.jogar(melhor_acao)
            primeira_jogada = False
            jogo.adiciona_historico_jogada(melhor_acao)
            jogo.printa_historico_jogada()
            jogo.atualiza_pontos_observaveis(melhor_acao)
            jogo.atualiza_tabuleiro()
            print(jogo)
        else:
            jogo.define_ou_inverte_jogador_atual()
            aprender(jogo)
            jogo, melhor_acao = jogar_melhor_recompensa(jogo)
            jogo.adiciona_historico_jogada(melhor_acao)
            jogo.printa_historico_jogada()
            jogo.atualiza_pontos_observaveis(melhor_acao)
            jogo.atualiza_tabuleiro()
            print(jogo)

        if verifica_venceu(jogo) and numero_treino != quantidade:
            print(f"Vitoria treino {numero_treino}: {Gomoku.turno_atual}")
            numero_treino += 1
            qntd_vitorias_qlearning += 1
            reseta_tabuleiro()
            primeira_jogada = True
            continue
        elif verifica_venceu(jogo) and numero_treino == quantidade:
            print(f"Vitoria treino {numero_treino}: {Gomoku.turno_atual}")
            qntd_vitorias_qlearning += 1
            reseta_tabuleiro()
            break

        jogada = melhor_jogada_agente(jogo, 2)
        jogo = jogo.jogar(jogada)

        jogo.adiciona_historico_jogada(jogada)
        jogo.printa_historico_jogada()
        jogo.atualiza_pontos_observaveis(jogada)
        jogo.atualiza_tabuleiro()
        print(jogo)

        if verifica_venceu(jogo) and numero_treino != quantidade:
            print(f"Vitoria treino {numero_treino}: {Gomoku.turno_atual}")
            numero_treino += 1
            qntd_vitorias_minimax += 1
            reseta_tabuleiro()
            primeira_jogada = True
            continue
        elif verifica_venceu(jogo) and numero_treino == quantidade:
            print(f"Vitoria treino {numero_treino}: {Gomoku.turno_atual}")
            qntd_vitorias_minimax += 1
            reseta_tabuleiro()
            break

    print("=-= Resultado final =-=")
    print(f"Q-Learning: {qntd_vitorias_qlearning} | Minimax: {qntd_vitorias_minimax}")  # noqa: E501

    jogo.limpa_historico_jogada()
    salvar_q_table()


def treino_qlearning_vs_qlearning(quantidade):
    Gomoku.ia_vs_ia = True

    Gomoku.alpha = 0.7
    Gomoku.gamma = 0.3
    Gomoku.epsilon = 0.9

    carregar_q_table()
    jogo = Gomoku()

    primeira_jogada = True

    numero_treino = 1
    qntd_vitorias_branco = 0
    qntd_vitorias_preto = 0

    while True:
        if primeira_jogada:
            jogo = Gomoku()
            jogo.define_ou_inverte_jogador_atual()
            melhor_acao = 112
            jogo = jogo.jogar(melhor_acao)
            primeira_jogada = False
            jogo.adiciona_historico_jogada(melhor_acao)
            jogo.printa_historico_jogada()
            jogo.atualiza_pontos_observaveis(melhor_acao)
            jogo.atualiza_tabuleiro()
            print(jogo)
        else:
            jogo.define_ou_inverte_jogador_atual()
            aprender(jogo)
            jogo, melhor_acao = jogar_aleatorio_recompensa(jogo)
            jogo.adiciona_historico_jogada(melhor_acao)
            jogo.printa_historico_jogada()
            jogo.atualiza_pontos_observaveis(melhor_acao)
            jogo.atualiza_tabuleiro()
            print(jogo)

        if verifica_venceu(jogo) and numero_treino != quantidade:
            print(f"Vitoria treino {numero_treino}: {Gomoku.turno_atual}")
            numero_treino += 1
            qntd_vitorias_branco += 1
            reseta_tabuleiro()
            primeira_jogada = True
            continue
        elif verifica_venceu(jogo) and numero_treino == quantidade:
            print(f"Vitoria treino {numero_treino}: {Gomoku.turno_atual}")
            qntd_vitorias_branco += 1
            reseta_tabuleiro()
            break

        jogo.define_ou_inverte_jogador_atual()
        aprender(jogo)
        jogo, melhor_acao = jogar_aleatorio_recompensa(jogo)

        jogo.adiciona_historico_jogada(melhor_acao)
        jogo.printa_historico_jogada()
        jogo.atualiza_pontos_observaveis(melhor_acao)
        jogo.atualiza_tabuleiro()
        print(jogo)

        if verifica_venceu(jogo) and numero_treino != quantidade:
            print(f"Vitoria treino {numero_treino}: {Gomoku.turno_atual}")
            numero_treino += 1
            qntd_vitorias_preto += 1
            reseta_tabuleiro()
            primeira_jogada = True
            continue
        elif verifica_venceu(jogo) and numero_treino == quantidade:
            print(f"Vitoria treino {numero_treino}: {Gomoku.turno_atual}")
            qntd_vitorias_preto += 1
            reseta_tabuleiro()
            break

    print("=-= Resultado final =-=")
    print(f"{Quadrado.B}: {qntd_vitorias_branco} | {Quadrado.P}: {qntd_vitorias_preto}")  # noqa: E501

    jogo.limpa_historico_jogada()
    salvar_q_table()
