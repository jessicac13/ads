import numpy as np
import pandas as pd
from scipy.linalg import null_space
import random


# -----------------------------
# Parâmetros do sistema
# -----------------------------
lambda1 = 10  # chegada T1
lambda2 = 15  # chegada T2
mi1 = 15      # atendimento T1
mi2 = 25      # atendimento T2
C = 5         # capacidade total
R = 2         # reserva para T1

# -----------------------------
# Lista de estados válidos
# -----------------------------
states = [
    (0,0), (0,1), (0,2), (0,3),
    (1,0), (1,1), (1,2), (1,3),
    (2,0), (2,1), (2,2), (2,3),
    (3,0), (3,1), (3,2),
    (4,0), (4,1),
    (5,0)
]

index_map = {state: i for i, state in enumerate(states)}
n = len(states)
Q = np.zeros((n, n))

# -----------------------------
# Construir matriz Q
# -----------------------------
for i, (n1, n2) in enumerate(states):
    # Entrada de T1
    next_state = (n1 + 1, n2)
    if next_state in index_map:
        Q[i][index_map[next_state]] = lambda1

    # Entrada de T2
    next_state = (n1, n2 + 1)
    if next_state in index_map:
        Q[i][index_map[next_state]] = lambda2

    # Saída de T1
    if n1 > 0:
        next_state = (n1 - 1, n2)
        Q[i][index_map[next_state]] = n1 * mi1

    # Saída de T2
    if n2 > 0:
        next_state = (n1, n2 - 1)
        Q[i][index_map[next_state]] = n2 * mi2

    # Diagonal principal
    Q[i][i] = -np.sum(Q[i])

# -----------------------------
# Exibir matriz Q com pandas
# -----------------------------
state_labels = [f"({n1},{n2})" for (n1, n2) in states]
Q_df = pd.DataFrame(Q, index=state_labels, columns=state_labels)

# Mostrar matriz no console
print(Q_df.round(2))

# -----------------------------
# Calcular distribuição estacionária π
# -----------------------------
# Transpor Q para resolver Qᵗ · πᵗ = 0
Q_t = Q.T
ns = null_space(Q_t)

# Normalizar π (soma = 1)
pi = ns[:, 0]
pi = pi / np.sum(pi)

# -----------------------------
# Imprimir resultados π
# -----------------------------
print("\nDistribuição estacionária π:")
for i, prob in enumerate(pi):
    print(f"π[{i}]  Estado {states[i]} = {prob:.6f}")

# Conjunto dos índices que satisfazem n2=3 ou n1+n2=5
indices_cond = [i for i, (n1, n2) in enumerate(states) if (n2 == 3) or (n1 + n2 == 5)]

# Soma das probabilidades π para esses estados
soma_prob = np.sum(pi[indices_cond])

print(f"\nSoma das probabilidades para estados com n2=3 ou n1+n2=5: {soma_prob:.6f}")


# -----------------------------
# Indicadores de desempenho
# -----------------------------
utilizacao_total = 0
conexoes_t1 = 0
conexoes_t2 = 0
tempo_cap_max = 0

for i, (n1, n2) in enumerate(states):
    prob = pi[i]
    utilizacao_total += (n1 + n2) * prob
    conexoes_t1 += n1 * prob
    conexoes_t2 += n2 * prob
    if n1 + n2 == C:
        tempo_cap_max += prob

print(f"\nUtilização média do sistema: {utilizacao_total:.6f}")
print(f"Número médio de conexões T1: {conexoes_t1:.6f}")
print(f"Número médio de conexões T2: {conexoes_t2:.6f}")
print(f"Fração do tempo em capacidade máxima (n1+n2={C}): {tempo_cap_max:.6f}")

# -----------------------------
# Simulação da CTMC
# -----------------------------
T_total = 10000  # Tempo total de simulação (em minutos)
tempo = 0.0
estado_atual = (0, 0)
index_atual = index_map[estado_atual]
tempo_estado = np.zeros(n)

while tempo < T_total:
    taxas = Q[index_atual].copy()
    taxas[index_atual] = 0  # Remover diagonal
    taxa_total = -Q[index_atual][index_atual]

    if taxa_total == 0:
        break  # Estado absorvente (não é o caso aqui)

    # Tempo de permanência ~ exponencial(taxa_total)
    delta_t = np.random.exponential(scale=1/taxa_total)
    
    # Acumular tempo no estado atual
    tempo_estado[index_atual] += delta_t
    tempo += delta_t

    # Probabilidades normalizadas de transição
    probs = taxas / taxa_total
    proximo_index = np.random.choice(n, p=probs)

    # Atualizar o estado
    index_atual = proximo_index

# -----------------------------
# Estimar distribuição π̂
# -----------------------------
pi_hat = tempo_estado / np.sum(tempo_estado)

print("\nEstimativa de π por simulação (π̂):")
for i, prob in enumerate(pi_hat):
    print(f"π̂[{i}]  Estado {states[i]} = {prob:.6f}")

# -----------------------------
# Comparar π (analítico) vs π̂ (simulado)
# -----------------------------
erro_abs = np.abs(pi - pi_hat)
erro_medio = np.mean(erro_abs)

print(f"\nErro absoluto médio entre π e π̂: {erro_medio:.6f}")

# Mostrar diferenças por estado
print("\nDiferença entre π e π̂ por estado:")
for i, (p_analitico, p_simulado) in enumerate(zip(pi, pi_hat)):
    print(f"Estado {states[i]}: |π - π̂| = {abs(p_analitico - p_simulado):.6f}")


