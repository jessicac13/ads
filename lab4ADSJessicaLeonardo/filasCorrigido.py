import matplotlib.pyplot as plt
import math

# *********************************
# Cenário atual (M/M/1)
mi = 180
lambdac = 150

e_n = lambdac / (mi - lambdac)
e_r = e_n / lambdac
e_wq = lambdac / (mi * (mi - lambdac))
ro = lambdac / mi

print('E_N= ', e_n)
print('E_R (tempo médio no sistema)= ', e_r)
print('E_Wq (tempo médio na fila) = ', e_wq)
print('Utilização do sistema = ', ro)

# *********************************
# Alternativa (i): 5 servidores independentes (cada um M/M/1)
lambda1 = 30
mi1 = 40

e_n1 = lambda1 / (mi1 - lambda1)
e_r1 = e_n1 / lambda1
e_wq1 = lambda1 / (mi1 * (mi1 - lambda1))
ro1 = lambda1 / mi1

print('\nE_N1= ', e_n1)
print('E_R1 (tempo médio no sistema)= ', e_r1)
print('E_Wq1 (tempo médio na fila)= ', e_wq1)
print('Utilização do sistema = ', ro1)

# *********************************
# Alternativa (ii): Fila única com 5 servidores (M/M/c)

c = 5
lambda2 = 150  # carga total recebida
mu = 40        # taxa de atendimento por servidor
ro2 = lambda2 / (c * mu)  # utilização do sistema

# Cálculo de P0 (probabilidade do sistema vazio)
sum_terms = sum((lambda2/mu)**n / math.factorial(n) for n in range(c))
last_term = ((lambda2/mu)**c) / (math.factorial(c) * (1 - ro2))
P0 = 1 / (sum_terms + last_term)

# Probabilidade da fila não estar vazia (Pfila)
Pfila = (((lambda2/mu)**c) / (math.factorial(c) * (1 - ro2))) * P0

# Tempo médio na fila Wq
Wq2 = Pfila / (c * mu - lambda2)

# Tempo médio no sistema W
W2 = Wq2 + 1/mu

# Número médio de clientes no sistema (Little's Law)
N2 = lambda2 * W2

print('\nAlternativa (ii) - Fila única M/M/c')
print(f'Utilização do sistema (ρ) = {ro2:.4f}')
print(f'P0 = {P0:.4f}')
print(f'Probabilidade fila (Pfila) = {Pfila:.4f}')
print(f'Tempo médio na fila (Wq) = {Wq2:.4f} min')
print(f'Tempo médio no sistema (W) = {W2:.4f} min')
print(f'Número médio de clientes no sistema (N) = {N2:.4f}')

# *********************************
# Gráfico comparativo
cenarios = ['Atual', '5 Servidores\nIndependentes', 'Fila Única\ncom 5 Servidores']
E_N = [e_n, e_n1, N2]
E_R = [e_r, e_r1, W2]
E_Wq = [e_wq, e_wq1, Wq2]
rho = [ro, ro1, ro2]

bar_width = 0.2
x = range(len(cenarios))

plt.figure(figsize=(10, 6))

plt.bar([i - 1.5 * bar_width for i in x], E_N, width=bar_width, label='Número médio no sistema (N)')
plt.bar([i - 0.5 * bar_width for i in x], E_R, width=bar_width, label='Tempo médio no sistema (W)')
plt.bar([i + 0.5 * bar_width for i in x], E_Wq, width=bar_width, label='Tempo médio na fila (Wq)')
plt.bar([i + 1.5 * bar_width for i in x], rho, width=bar_width, label='Utilização (ρ)')

plt.xticks(x, cenarios)
plt.ylabel('Valores')
plt.title('Comparação de Métricas por Cenário')
plt.legend()
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()
