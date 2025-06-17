import heapq
import numpy as np

# ----------------------------
# Classe base de eventos
# ----------------------------
class Event:
    def __init__(self, time):
        self.time = time

    def __lt__(self, other):
        return self.time < other.time

    def processing_event(self, simulator):
        raise NotImplementedError

# ----------------------------
# Simulador com lista de eventos
# ----------------------------
class Simulator:
    def __init__(self, end_time):
        self.current_time = 0
        self.event_queue = []
        self.end_time = end_time
        self.filas = {}
        self.metrics = {}

    def schedule(self, event):
        heapq.heappush(self.event_queue, event)

    def run(self):
        while self.event_queue and self.current_time < self.end_time:
            event = heapq.heappop(self.event_queue)
            self.current_time = event.time
            event.processing_event(self)

# ----------------------------
# Classe Cliente
# ----------------------------
class Cliente:
    def __init__(self, arrival_time):
        self.arrival_time = arrival_time

# ----------------------------
# Classe Fila M/M/1
# ----------------------------
class Fila:
    def __init__(self, nome, taxa_servico):
        self.nome = nome
        self.taxa_servico = taxa_servico
        self.fila = []
        self.ocupado = False
        self.total_respondido = 0
        self.total_resposta = 0.0
        self.tempo_ocupado = 0.0
        self.last_busy_time = 0.0

    def chegada(self, cliente, simulator):
        self.fila.append(cliente)
        if not self.ocupado:
            self.iniciar_servico(simulator)

    def iniciar_servico(self, simulator):
        if self.fila:
            cliente = self.fila.pop(0)
            self.ocupado = True
            self.last_busy_time = simulator.current_time
            duracao = np.random.exponential(1 / self.taxa_servico)
            simulator.schedule(DepartureEvent(simulator.current_time + duracao, self.nome, cliente))

    def saida(self, cliente, simulator):
        self.ocupado = False
        tempo_resposta = simulator.current_time - cliente.arrival_time
        self.total_respondido += 1
        self.total_resposta += tempo_resposta
        self.tempo_ocupado += simulator.current_time - self.last_busy_time
        self.iniciar_servico(simulator)

    def tempo_medio_resposta(self):
        if self.total_respondido == 0:
            return 0
        return self.total_resposta / self.total_respondido

    def utilizacao(self, tempo_total):
        return self.tempo_ocupado / tempo_total

# ----------------------------
# Eventos de chegada
# ----------------------------
class ArrivalEvent(Event):
    def __init__(self, time, fila_nome):
        super().__init__(time)
        self.fila_nome = fila_nome

    def processing_event(self, simulator):
        cliente = Cliente(simulator.current_time)
        fila = simulator.filas[self.fila_nome]
        fila.chegada(cliente, simulator)

        # Reagendamento da chegada
        if self.fila_nome == "fila1":
            taxa = 10  # λ1
        else:
            return

        proxima_chegada = simulator.current_time + np.random.exponential(1 / taxa)
        simulator.schedule(ArrivalEvent(proxima_chegada, self.fila_nome))

# ----------------------------
# Evento de saída
# ----------------------------
class DepartureEvent(Event):
    def __init__(self, time, fila_nome, cliente):
        super().__init__(time)
        self.fila_nome = fila_nome
        self.cliente = cliente

    def processing_event(self, simulator):
        fila = simulator.filas[self.fila_nome]
        fila.saida(self.cliente, simulator)

        # Roteamento
        if self.fila_nome == "fila1":
            if np.random.rand() < 0.7:
                simulator.schedule(RoutingEvent(simulator.current_time, "fila2", self.cliente))
            else:
                pass  # perda: 30%
        elif self.fila_nome == "fila2":
            destino = "fila3" if np.random.rand() < 0.6 else "fila4"
            simulator.schedule(RoutingEvent(simulator.current_time, destino, self.cliente))

# ----------------------------
# Evento de roteamento
# ----------------------------
class RoutingEvent(Event):
    def __init__(self, time, fila_destino, cliente):
        super().__init__(time)
        self.fila_destino = fila_destino
        self.cliente = cliente

    def processing_event(self, simulator):
        simulator.filas[self.fila_destino].chegada(self.cliente, simulator)

# ----------------------------
# Execução da simulação
# ----------------------------
def main():
    sim = Simulator(end_time=1000)

    # Criar filas
    sim.filas["fila1"] = Fila("fila1", 30)
    sim.filas["fila2"] = Fila("fila2", 30)
    sim.filas["fila3"] = Fila("fila3", 30)
    sim.filas["fila4"] = Fila("fila4", 30)

    # Agendar primeiras chegadas
    sim.schedule(ArrivalEvent(0, "fila1"))
    
    # Executar simulação
    sim.run()

    # Mostrar resultados
    print(f"{'Fila':<10}{'Resposta (s)':<20}{'Utilização (%)':<20}{'Vazão (clientes/s)':<25}")
    for nome, fila in sim.filas.items():
        tempo_medio = fila.tempo_medio_resposta()
        utiliz = 100 * fila.utilizacao(sim.end_time)
        vazao = fila.total_respondido / sim.end_time
        print(f"{nome:<10}{tempo_medio:<20.4f}{utiliz:<20.2f}{vazao:<25.4f}")

if __name__ == "__main__":
    main()
