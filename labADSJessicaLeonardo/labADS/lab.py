import subprocess
import time
import random

def run_command(cmd):
    print(f"\nExecutando: {cmd}")
    subprocess.run(cmd, shell=True)

def get_ip(host):
    result = subprocess.check_output(f"sudo himage {host} ip -4 addr show eth0", shell=True).decode()
    for line in result.splitlines():
        if "inet" in line:
            return line.strip().split()[1].split('/')[0]
    return None

def get_eid(file: str) -> str:
    output = subprocess.check_output(f"sudo imunes -b {file} | grep 'ID'", shell=True)
    output = output.decode("utf-8")
    eid = output.split("\n")[-2].split(" = ")[1]
    return eid

def gera_ruido_udp(destino, duracao_total):
    elapsed = 0
    while elapsed < duracao_total:
        dur = random.randint(2, 6)
        taxa = random.randint(1, 10)
        print(f"[ UDP ] {taxa} Mbps por {dur} s")
        run_command(f"sudo himage {pc1} iperf -u -c {destino} -t {dur} -b {taxa}M")
        time.sleep(dur)
        elapsed += dur

def salva_csv(buffer, delay, repeticao, output):
    with open("resultadosComRepeticao.csv", "a") as f:
        f.write(f"Buffer={buffer},Delay={delay},Repeticao={repeticao}\n")
        f.write(output)
        f.write("\n")

file = "/home/aluno/labADS/topologiaLAB1.imn"

run_command("sudo imunes -b /home/aluno/labADS/topologiaLAB1.imn")

buffers = [64000, 208000]
delays = ['10000', '100000']
repeticoes = 8

exec_id = get_eid(file)

pc1 = f"pc1@{exec_id}"
pc2 = f"pc2@{exec_id}"
pc3 = f"pc3@{exec_id}"
pc4 = f"pc4@{exec_id}"

router1 = "router1"
router2 = "router2"

pc3_ip = get_ip(pc3)
pc4_ip = get_ip(pc4)

# Servidores
run_command(f"sudo himage {pc3} iperf -s -u &")
run_command(f"sudo himage {pc4} iperf -s &")

time.sleep(2)

for buffer in buffers:
    for delay in delays:
        for i in range(repeticoes):
            print(f"\n=== Teste {i+1} | Buffer: {buffer} | Delay: {delay} ===")

            # Aplica delay
            run_command(f"sudo vlink -e {exec_id} -dly {delay} router1:router2")

            # Teste TCP: captura saída em CSV
            output = subprocess.check_output(
                f"sudo himage {pc2} iperf -c {pc4_ip} -n 100M -w {buffer} -i 1 -y C",
                shell=True
            ).decode("utf-8")

            salva_csv(buffer, delay, i + 1, output)

            # Ruído UDP
            gera_ruido_udp(pc3_ip, 10)

            time.sleep(2)
