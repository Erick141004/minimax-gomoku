import pickle
import random
from gomoku import Gomoku


def busca_q_atual(estado, acao):
    return Gomoku.q_table.get((estado, acao), 0)


def escolher_acao(estado, possiveis_acoes):
    if random.random() < Gomoku.epsilon:
        return random.choice(possiveis_acoes)
    else:
        q_values = [busca_q_atual(estado, acao) for acao in possiveis_acoes]
        max_q_value = max(q_values)
        max_actions = [
            acao
            for acao, q_val in zip(possiveis_acoes, q_values)
            if q_val == max_q_value
        ]
        return random.choice(max_actions)


def atualizar_q_valor(estado, acao, recompensa, novo_estado, possiveis_acoes):
    q_atual = busca_q_atual(estado, acao)

    max_q_novo_estado = max(
        [busca_q_atual(novo_estado, nova_acao) for nova_acao in possiveis_acoes],  # noqa: E501

        default=0,
    )

    Gomoku.q_table[(estado, acao)] = q_atual + Gomoku.alpha * (
        recompensa + Gomoku.gamma * max_q_novo_estado - q_atual
    )


def aprender(jogo: Gomoku):
    estado = jogo.estado_chave_qlearning()
    possiveis_acoes = list(jogo.pontos_observaveis)

    acao = escolher_acao(estado, possiveis_acoes)

    novo_estado = jogo.jogar(acao)
    novo_estado.atualiza_pontos_observaveis(acao, qlearning=True)

    recompensa = novo_estado.calcular_utilidade(jogo.turno_atual, acao)
    atualizar_q_valor(
        estado,
        acao,
        recompensa,
        novo_estado.estado_chave_qlearning(),
        list(novo_estado.pontos_observaveis),
    )


def jogar_melhor_recompensa(jogo: Gomoku):
    estado_chave = jogo.estado_chave_qlearning()
    lista = [(x, y) for x, y in Gomoku.q_table.items() if x[0] == estado_chave]
    lista.sort(key=lambda x: x[1], reverse=True)

    melhor_acao = lista[0][0][1]

    return jogo.jogar(melhor_acao), melhor_acao


def estado_na_lista(jogo: Gomoku):
    existe = False

    estado = jogo.estado_chave_qlearning()

    for key in Gomoku.q_table.keys():
        if key[0] == estado:
            existe = True

    return existe


def salvar_q_table():
    with open("q_table.pkl", "wb") as f:
        pickle.dump(Gomoku.q_table, f)


def carregar_q_table():
    with open("q_table.pkl", "rb") as f:
        Gomoku.q_table = pickle.load(f)
