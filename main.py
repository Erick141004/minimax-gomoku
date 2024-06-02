from tipos_jogos import (
    humano_vs_humano,
    humano_vs_minimax,
    humano_vs_minimax_qlearning,
    humano_vs_qlearning,
    qlearning_vs_minimax,
    reseta_tabuleiro,
    treino_qlearning_vs_minimax,
    treino_qlearning_vs_qlearning,
)


if __name__ == "__main__":

    opcao = -1
    again = -1

    while opcao != 0:
        print("Escolha um modo de jogo:")
        print("1 - Humano vs Humano")
        print("2 - Humano vs Minimax")
        print("3 - Humano vs Q-Learning")
        print("4 - Humano vs Minimax e Q-Learning")
        print("5 - Q-Learning vs Minimax")
        print("6 - TREINO Q-Learning vs Minimax")
        print("7 - TREINO Q-Learning vs Q-Learning")
        print("0 - Sair")
        opcao = input()

        match opcao:
            case "1":
                humano_vs_humano()
                again = 0
            case "2":
                humano_vs_minimax()
                again = 0
            case "3":
                humano_vs_qlearning()
                again = 0
            case "4":
                humano_vs_minimax_qlearning()
                again = 0
            case "5":
                qlearning_vs_minimax()
                again = 0
            case "6":
                quantidade = int(
                    input("Escreva a quantidade de partidadas para treinar (numero)\n")  # noqa: E501
                )
                treino_qlearning_vs_minimax(quantidade)
                again = 0
            case "7":
                quantidade = int(
                    input("Escreva a quantidade de partidadas para treinar (numero)\n")  # noqa: E501
                )
                treino_qlearning_vs_qlearning(quantidade)
                again = 0
            case "0":
                opcao = 0

            case default:
                print("Opcao invalida")

        while again == 0:

            resposta = input("Deseja jogar novamente? S/N\n")

            primeira_letra = resposta[0].lower()

            match primeira_letra:
                case "s":
                    reseta_tabuleiro()
                    again = 1
                case "n":
                    again = 1
                    opcao = 0
                case default:
                    print("Opcao invalida")
