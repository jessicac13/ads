# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

# Matriz de transição
P = np.array([
    [0.6, 0.4, 0.0],
    [0.2, 0.5, 0.3],
    [0.2, 0.4, 0.4]
])

n_steps = 1000
states = [0]  # começa no estado ocioso

# Simulação da cadeia de Markov
for _ in range(n_steps - 1):
    current_state = states[-1]
    next_state = np.random.choice([0, 1, 2], p=P[current_state])
    states.append(next_state)

# Cria um DataFrame com índice de 0 a 999
df = pd.DataFrame({'Estado': states})

# Salva como planilha CSV
df.to_csv("cadeia_markov.csv", index_label="Passo")

print("Arquivo 'cadeia_markov.csv' gerado com sucesso.")
