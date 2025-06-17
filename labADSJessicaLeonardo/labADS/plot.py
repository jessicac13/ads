import matplotlib.pyplot as plt

# Dados
labels = [
    "64 KB, 10 ms",
    "64 KB, 100 ms",
    "208 KB, 10 ms",
    "208 KB, 100 ms"
]

bandwidth = [
    46815714.375,
    33614182.625,
    137508821.5,
    78725323.5
]

# Plot
plt.figure(figsize=(10, 6))
plt.bar(labels, bandwidth, color='skyblue')
plt.title("Bandwidth (Bytes/s) para diferentes tamanhos e tempos")
plt.xlabel("Tamanho x Tempo")
plt.ylabel("Bandwidth (Bytes/s)")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
