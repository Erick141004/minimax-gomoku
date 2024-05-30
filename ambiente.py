import numpy as np

class Ambiente:
  def __init__(self):
    self.estados = np.array([])
    self.acoes = np.array([])

  # descrever
  def T(self, estado, acao):
   return []

  # Recompensas
  def R(self, estado, acao, proximo_estado):
    return 0

  # Como o problema deve se imprimir
  # ou como deve mostrar o espaço de estados
  def __str__(self):
    return self

  def imprimir_valor(self, V):
    return ""

  def imprimir_politica(self, politica):
    return ""