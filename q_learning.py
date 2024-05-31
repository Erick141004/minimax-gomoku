import pickle
import random
from gomoku import Gomoku


def busca_q_atual(estado, acao):
    """Pega o valor Q para um par estado-acao. Se nao existir, retorna 0."""
    return Gomoku.q_table.get((tuple(estado), acao), 0)


def escolher_acao(estado, possiveis_acoes):
    """Decide entre explorar acoes aleatorias ou a melhor acao conhecida."""
    if random.random() < Gomoku.epsilon:
        return random.choice(possiveis_acoes)  # Exploracao
    else:
        # Explora a melhor acao com base nos valores Q conhecidos
        q_values = [busca_q_atual(estado, acao) for acao in possiveis_acoes]
        max_q_value = max(q_values)
        # Pode ter mais de uma acao com valor maximo Q, escolhe uma aleatoriamente
        max_actions = [
            acao
            for acao, q_val in zip(possiveis_acoes, q_values)
            if q_val == max_q_value
        ]
        return random.choice(max_actions)


def atualizar_q_valor(estado, acao, recompensa, novo_estado, possiveis_acoes):
    """Atualiza o valor Q usando a equacao de Bellman."""
    q_atual = busca_q_atual(estado, acao)
    max_q_novo_estado = max(
        [busca_q_atual(novo_estado, nova_acao) for nova_acao in possiveis_acoes],
        default=0,
    )
    # Equacao de Bellman
    Gomoku.q_table[(tuple(estado), acao)] = q_atual + Gomoku.alpha * (
        recompensa + Gomoku.gamma * max_q_novo_estado - q_atual
    )


def aprender(jogo: Gomoku):
    """Processo de aprendizado para um episodio."""

    estado = jogo.estado_chave_qlearning()
    possiveis_acoes = list(jogo.pontos_observaveis)

    print("Escolhendo acao...")
    acao = escolher_acao(estado, possiveis_acoes)
    print(f"Acao escolhida: {acao}")
    if acao:

        novo_estado = jogo.jogar(acao)
        novo_estado.atualiza_pontos_observaveis(acao, qlearning=True)

        if novo_estado:
            recompensa = novo_estado.calcular_utilidade(jogo.turno_atual, acao)
            print(f"Recompensa: {recompensa}")
            atualizar_q_valor(
                estado,
                acao,
                recompensa,
               novo_estado.estado_chave_qlearning(),
                list(novo_estado.pontos_observaveis),
            )  # Passa possiveis acoes para atualizar
            return True
        else:
            print("Movimento falhou.")
    else:
        print("Nenhuma acao valida encontrada.")
    return False


# Funções para uso com Pickle
def salvar_q_table():
    with open("q_table.pkl", "wb") as f:
        pickle.dump(Gomoku.q_table, f)


def carregar_q_table() -> dict:
    with open("q_table.pkl", "rb") as f:
        return pickle.load(f)
