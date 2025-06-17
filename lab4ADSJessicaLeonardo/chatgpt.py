import math
import pandas as pd

# ---------- Funções para M/M/1 ----------
def mm1_metrics(lambd, mu):
    rho = lambd / mu
    W = 1 / (mu - lambd)             # Tempo médio no sistema
    Wq = lambd / (mu * (mu - lambd)) # Tempo médio na fila
    Ws = 1 / mu                      # Tempo de atendimento
    return rho, W, Wq, Ws

# ---------- Função para M/M/c ----------
def mmc_metrics(lambd, mu, c):
    rho = lambd / (c * mu)

    # Cálculo da probabilidade de 0 na fila (P0)
    sum_terms = sum((lambd / mu) ** n / math.factorial(n) for n in range(c))
    last_term = ((lambd / mu) ** c) / (math.factorial(c) * (1 - rho))
    P0 = 1 / (sum_terms + last_term)

    # Probabilidade de haver espera na fila (Erlang-C)
    Pw = last_term * P0

    # Tempo médio na fila
    Wq = Pw * (1 / mu) / (c * (1 - rho))
    W = Wq + 1 / mu
    Ws = 1 / mu
    return rho, W, Wq, Ws

# ---------- Parâmetros ----------
lambda_total = 150
mu_atual = 180

# Configuração atual (1 servidor M/M/1)
rho_1, W_1, Wq_1, Ws_1 = mm1_metrics(lambda_total, mu_atual)

# Alternativa (i): 5 servidores M/M/1
lambda_indiv = 30
mu_indiv = 40
rho_i, W_i, Wq_i, Ws_i = mm1_metrics(lambda_indiv, mu_indiv)

# Alternativa (ii): Fila única M/M/5
c = 5
mu_multi = 40
rho_ii, W_ii, Wq_ii, Ws_ii = mmc_metrics(lambda_total, mu_multi, c)

# ---------- Construção da Tabela ----------
df = pd.DataFrame({
    "Configuração": ["Atual (1 servidor)", "5 Servidores M/M/1", "Fila Única M/M/5"],
    "Utilização (ρ)": [rho_1, rho_i, rho_ii],
    "Tempo total no sistema (W) [min]": [W_1, W_i, W_ii],
    "Tempo na fila (Wq) [min]": [Wq_1, Wq_i, Wq_ii],
    "Tempo de atendimento (Ws) [min]": [Ws_1, Ws_i, Ws_ii]
})

# ---------- Resultados ----------
print(df.round(4))
