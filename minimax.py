def minimax(jogo, turno_max, jogador, profundidade_maxima, prox_jogo):
    # se o jogo acabou ou se a profundidade é máxima
    if jogo.venceu() or jogo.empate() or profundidade_maxima == 0:
        return jogo.calcular_utilidade(jogador, prox_jogo)

    if turno_max:  # turno do MAX
        melhor_valor = float("-inf")  # Menos infinito é o menor valor
        for proximo_jogo in jogo.atualiza_pontos_observaveis_simulacao(prox_jogo):
            utilidade = minimax(jogo.jogar(proximo_jogo), False, jogador, profundidade_maxima - 1, prox_jogo)
            print(
                f"MAX vai escolher entre a utilidade {utilidade} e o {melhor_valor} - Utilidade corresponde a casa: {proximo_jogo}")
            melhor_valor = max(utilidade, melhor_valor)  # proximo_jogo com o maior valor

        return melhor_valor
    else:  # turno no MIN
        pior_valor = float("inf")  # Mais infinito é o maior valor
        for proximo_jogo in jogo.atualiza_pontos_observaveis_simulacao(prox_jogo):
            utilidade = minimax(jogo.jogar(proximo_jogo), True, jogador, profundidade_maxima - 1, prox_jogo)
            print(
                f"MIN vai escolher entre a utilidade {utilidade} e o {pior_valor} - Utilidade corresponde a casa: {proximo_jogo}")
            pior_valor = min(utilidade, pior_valor)  # proximo_jogo com o menor valor
        return pior_valor


def minimax_alfabeta(jogo, turno_max, jogador, profundidade_maxima, prox_jogo, alfa=float("-inf"), beta=float("inf")):
    # se o jogo acabou ou se a profundidade é máxima
    if jogo.venceu() or jogo.empate() or profundidade_maxima == 0:
        return jogo.calcular_utilidade(jogador, prox_jogo)

    if turno_max:  # turno do MAX
        for proximo_jogo in jogo.atualiza_pontos_observaveis_simulacao(prox_jogo):
            utilidade = minimax_alfabeta(jogo.jogar(proximo_jogo), False, jogador, profundidade_maxima - 1, prox_jogo,
                                         alfa, beta)
            alfa = max(utilidade, alfa)
            if beta <= alfa:
                continue
            return alfa
    else:  # turno no MIN
        for proximo_jogo in jogo.atualiza_pontos_observaveis_simulacao(prox_jogo):
            utilidade = minimax_alfabeta(jogo.jogar(proximo_jogo), True, jogador, profundidade_maxima - 1, prox_jogo,
                                         alfa, beta)
            beta = min(utilidade, beta)
            if beta <= alfa:
                continue
            return beta


# Encotrar o melhor movimento do computador
def melhor_jogada_agente(jogo, profundidade_maxima):
    melhor_valor = float("-inf")
    melhor_jogada = -1
    for proximo_jogo in jogo.pontos_observaveis:
        utilidade = minimax(jogo.jogar(proximo_jogo), False, jogo.turno(), profundidade_maxima, proximo_jogo)
        if utilidade > melhor_valor:
            melhor_valor = utilidade
            melhor_jogada = proximo_jogo
    return melhor_jogada


def melhor_jogada_agente_poda(jogo, profundidade_maxima):
    melhor_valor = float("-inf")
    melhor_jogada = -1
    for proximo_jogo in jogo.pontos_observaveis:
        utilidade = minimax_alfabeta(jogo.jogar(proximo_jogo), False, jogo.turno(), profundidade_maxima, proximo_jogo)
        if utilidade > melhor_valor:
            melhor_valor = utilidade
            melhor_jogada = proximo_jogo
    return melhor_jogada
