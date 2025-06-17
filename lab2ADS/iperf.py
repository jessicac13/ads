import subprocess
import time
import os
import csv

# Garante que o arquivo CSV final exista e tenha cabeçalho
output_csv = "resultadosIPERF.csv"
if not os.path.exists(output_csv):
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Passo", "Estado", "saida_iperf"])

# Alvo do iperf
DESTINO = "191.36.15.1"

# Lê os estados do CSV de entrada
with open("/home/jessica/Eng/ADS/lab2ADS/cadeia_markov.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        passo = int(row['Passo'])
        estado = int(row['Estado'])

        print(f"Estado {estado} - segundo {passo * 10}")

        if estado == 1:
            cmd = f"iperf -c {DESTINO} -b 10M -t 10"
        elif estado == 2:
            cmd = f"iperf -c {DESTINO} -b 50M -t 10"
        else:
            time.sleep(10)

            # Salva estado ocioso no CSV
            with open(output_csv, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([passo, estado, "Ocioso"])
            continue

        # Executa o comando e captura a saída
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = result.stdout.decode()

        # Salva resultado no CSV
        with open(output_csv, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([passo, estado, output.strip()])
