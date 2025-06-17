import matplotlib.pyplot as plt

# *********************************
# Cenário atual
mi = 180
lambdac = 150

e_n = lambdac / ( mi - lambdac)
e_r = e_n / lambdac
e_wq = lambdac / (mi * (mi - lambdac))
ro = lambdac / mi

print('E_N= ', e_n)
print('E_R (tempo médio no sistema)= ', e_r)
print('E_Wq (tempo médio na fila) = ', e_wq)
print('Utilização do sistema = ', ro)

# *********************************
# Alternativa (i): 5 servidores independentes
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
# Alternativa (ii): Fila única com 5 servidores
c = 5
lambda2 = 30 * c
mi2 = 40 * c

e_n2 = lambda2 / (mi2 - lambda2)
e_r2 = e_n2 / lambda2
e_wq2 = lambda2 / (mi2 * (mi2 - lambda2))
ro2 = lambda2 / mi2

print('\nE_N2= ', e_n2)
print('E_R2 (tempo médio no sistema)= ', e_r2)
print('E_Wq2 (tempo médio na fila)= ', e_wq2)
print('Utilização do sistema = ', ro2)

# *********************************
# Gráfico comparativo
cenarios = ['Atual', '5 Servidores\nIndependentes', 'Fila Única\ncom 5 Servidores']
E_N = [e_n, e_n1, e_n2]
E_R = [e_r, e_r1, e_r2]
E_Wq = [e_wq, e_wq1, e_wq2]
rho = [ro, ro1, ro2]

bar_width = 0.2
x = range(len(cenarios))

plt.figure(figsize=(10, 6))

plt.bar([i - 1.5 * bar_width for i in x], E_N, width=bar_width, label='E_N (clientes)')
plt.bar([i - 0.5 * bar_width for i in x], E_R, width=bar_width, label='E_R (tempo no sistema)')
plt.bar([i + 0.5 * bar_width for i in x], E_Wq, width=bar_width, label='E_Wq (tempo na fila)')
plt.bar([i + 1.5 * bar_width for i in x], rho, width=bar_width, label='ρ (utilização)')

plt.xticks(x, cenarios)
plt.ylabel('Valores')
plt.title('Comparação de Métricas por Cenário')
plt.legend()
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()
