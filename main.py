import jogo_velha
from minimax import melhor_jogada_agente, melhor_jogada_agente_poda

if __name__ == "__main__":

    jogo = jogo_velha.JogoVelha()

    def jogada_humano():
        jogada = -1
        while jogada not in jogo.jogos_validos():
            jogada = int(input("Escolha um quadrado (0-8):"))
        return jogada

    while True:
        humano = jogada_humano()
        jogo = jogo.jogar(humano)
        if jogo.venceu():
            print("Humano Venceu!")
            break
        elif jogo.empate():
            print("Empate!")
            break
        computador = melhor_jogada_agente(jogo)
        print(f"Jogada do Computador é {computador}")
        jogo = jogo.jogar(computador)
        print(jogo)
        if jogo.venceu():
            print("Computador venceu!")
            break
        elif jogo.empate():
            print("Empate!")
            break
