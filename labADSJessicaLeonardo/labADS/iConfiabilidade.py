import matplotlib.pyplot as plt
import numpy as np

# Labels
labels = ["64 KB, 10 ms", "64 KB, 100 ms", "208 KB, 10 ms", "208 KB, 100 ms"]

# Vazões (médias)
vazoes = [46815714.375, 33614182.625, 137508821.5, 78725323.5]

# Intervalos de confiança (inferior e superior)
ic_inferior = [46743441.9595497, 24826911.4462866, 137207542.320366, 57594989.5767368]
ic_superior = [46887986.7904503, 42401453.8037134, 137810100.679634, 99855657.4232632]

# Calculando erros (diferença entre média e limite)
erro_inferior = [media - inf for media, inf in zip(vazoes, ic_inferior)]
erro_superior = [sup - media for media, sup in zip(vazoes, ic_superior)]

# Usando erro assimétrico (inferior e superior diferentes)
yerr = [erro_inferior, erro_superior]

# Plot
plt.figure(figsize=(10, 6))
plt.bar(labels, vazoes, yerr=yerr, capsize=10, color='lightblue', edgecolor='black')
plt.ylabel("Vazão (Bytes/s)")
plt.title("Vazão com Intervalos de Confiança")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
