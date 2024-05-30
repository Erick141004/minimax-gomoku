from copy import copy
from gomoku import Gomoku


# proximo_movimento eh a jogada imediata que estamos calculando a utilidade e proximo_jogo_simulacao sao as jogadas sucessoras  # noqa: E501
def minimax(jogo: Gomoku, turno_max: bool, jogador, profundidade_maxima, proximo_movimento, proximo_jogo_simulacao, pontos_observaveis_simulacao):  # noqa: E501

    jogo.atualiza_pontos_observaveis_simulacao(pontos_observaveis_simulacao, proximo_jogo_simulacao)  # noqa: E501

    # se o jogo acabou ou se a profundidade é máxima
    if jogo.venceu() or jogo.empate() or profundidade_maxima == 0 or not pontos_observaveis_simulacao:  # noqa: E501
        return jogo.calcular_utilidade(jogador, proximo_movimento)

    if turno_max:  # turno do MAX
        melhor_valor = float("-inf")  # Menos infinito é o menor valor
        for proximo_jogo in pontos_observaveis_simulacao:
            utilidade = minimax(
                jogo.jogar(proximo_jogo),
                False,
                jogador,
                profundidade_maxima - 1,
                proximo_movimento,
                proximo_jogo,
                copy(pontos_observaveis_simulacao)
            )

            # if proximo_movimento == 48:
            #     print(jogo)
            #     print(f"RETORNOU PRO MAX - Utilidade: {utilidade} - Melhor Valor: {melhor_valor}")
            #
            # a = melhor_valor
            # b = max(utilidade, melhor_valor)
            #
            # if proximo_movimento == 5 and a != b:
            #     print(f"Nova utilidade: {utilidade}")
            #     print(f"Atual melhor valor: {melhor_valor}")

            melhor_valor = max(
                utilidade, melhor_valor
            )  # proximo_jogo com o maior valor

            #print(f"MAX ESCOLHEU = {melhor_valor}")

        return melhor_valor
    else:  # turno no MIN
        pior_valor = float("inf")  # Mais infinito é o maior valor
        for proximo_jogo in pontos_observaveis_simulacao:
            utilidade = minimax(
                jogo.jogar(proximo_jogo),
                True,
                jogador,
                profundidade_maxima - 1,
                proximo_movimento,
                proximo_jogo,
                copy(pontos_observaveis_simulacao)
            )

            # if proximo_movimento == 48:
            #     print(jogo)
            #     print(f"RETORNOU PRO MIN - Utilidade: {utilidade} - Melhor Valor: {pior_valor}")

            pior_valor = min(utilidade, pior_valor)  # proximo_jogo com o menor valor  # noqa: E501

            # print(f"MIN ESCOLHEU = {pior_valor}")

        return pior_valor


def minimax_alfabeta(
    jogo,
    turno_max,
    jogador,
    profundidade_maxima,
    prox_jogo,
    # len_atualizado,
    alfa=float("-inf"),
    beta=float("inf"),
):

    pontos_observaveis_simulacao = jogo.atualiza_pontos_observaveis_simulacao(prox_jogo)  # noqa: E501

    # se o jogo acabou ou se a profundidade é máxima
    if jogo.venceu() or jogo.empate() or profundidade_maxima == 0 or not pontos_observaveis_simulacao:  # noqa: E501
        return jogo.calcular_utilidade(jogador, prox_jogo)

    if turno_max:  # turno do MAX

        for proximo_jogo in pontos_observaveis_simulacao:
            utilidade = minimax_alfabeta(
                jogo.jogar(proximo_jogo),
                False,
                jogador,
                profundidade_maxima - 1,
                prox_jogo,
                # True,
                alfa,
                beta,
            )
            alfa = max(utilidade, alfa)
            if beta <= alfa:
                continue
            return alfa
    else:  # turno no MIN

        for proximo_jogo in pontos_observaveis_simulacao:
            utilidade = minimax_alfabeta(
                jogo.jogar(proximo_jogo),
                True,
                jogador,
                profundidade_maxima - 1,
                prox_jogo,
                # True,
                alfa,
                beta,
            )
            beta = min(utilidade, beta)
            if beta <= alfa:
                continue
            return beta


# Encotrar o melhor movimento do computador
def melhor_jogada_agente(jogo: Gomoku, profundidade_maxima: int):

    Gomoku.turno_atual = Gomoku.turno_atual.oposto()

    melhor_valor = float("-inf")
    melhor_jogada = -1
    for proximo_jogo in jogo.pontos_observaveis:
        utilidade = minimax(
            jogo.jogar(proximo_jogo),
            False,
            jogo.turno(),
            profundidade_maxima,
            proximo_jogo,  # proximo_movimento
            proximo_jogo,  # proximo_jogo_simulacao
            set()
        )

        #print(f"ESCOLHA ENTRE: UTILIDADE = {utilidade} - MELHOR VALOR = {melhor_valor} - NA CASA = {proximo_jogo}")

        if utilidade > melhor_valor:
            melhor_valor = utilidade
            melhor_jogada = proximo_jogo

    #print(f"Jogada agente: {melhor_jogada} | Utilidade: {melhor_valor}")
    return melhor_jogada


def melhor_jogada_agente_poda(jogo, profundidade_maxima):

    Gomoku.turno_atual = Gomoku.turno_atual.oposto()

    melhor_valor = float("-inf")
    melhor_jogada = -1
    for proximo_jogo in jogo.pontos_observaveis:
        utilidade = minimax_alfabeta(
            jogo.jogar(proximo_jogo),
            False,
            jogo.turno(),
            profundidade_maxima,
            proximo_jogo,
            # False,
        )
        if utilidade > melhor_valor:
            melhor_valor = utilidade
            melhor_jogada = proximo_jogo
    return melhor_jogada
