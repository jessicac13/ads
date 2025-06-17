import pandas as pd

# Lê os resultados do iperf
df = pd.read_csv("resultadosIPERF.csv")

# Função para extrair a taxa de transmissão (Mbps) de cada linha de 'saida_iperf'
def extract_bandwidth(iperf_output):
    # Procura por 'Mbits/sec' na saída e extrai o número anterior
    if "Mbits/sec" in iperf_output:
        # Divide a string e extrai o valor correspondente
        parts = iperf_output.split()
        for i, part in enumerate(parts):
            if "Mbits/sec" in part:
                # Retorna o valor de transferência em Mbits/sec
                return float(parts[i-1])
    return 0  # Caso não encontre, retorna 0

# Aplica a função para extrair a taxa de cada linha
df['Vazao'] = df['saida_iperf'].apply(extract_bandwidth)

# Exibe as primeiras linhas para ver como ficou
print(df.head())

# Calcula a vazão média
vazao_media_pratica = df['Vazao'].mean()
print(f"Vazão média prática: {vazao_media_pratica} Mbps")

# Calcula a proporção de tempo em cada estado
estado_counts = df['Estado'].value_counts(normalize=True)
print("Proporção de tempo em cada estado:")
print(estado_counts)
