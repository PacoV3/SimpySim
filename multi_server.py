from numpy.random import exponential, normal
from numpy import average
import matplotlib.pyplot as plt
import simpy


class ProductionLine:
    def __init__(self, env, bcs):
        self.env = env # Lo que hace que funcione simpy
        self.bcs = bcs # Recurso para procesar las piezas
        self.inspection_times = [] # Tiempo en el sistema para todas las piezas

    def piece(self, name, arriving_time, inspect_time):
        yield self.env.timeout(arriving_time)
        with self.bcs.request() as req:
            yield req
            yield self.env.timeout(inspect_time)
            self.inspection_times.append(self.env.now - arriving_time)

    def build_simulation_by_time(self, max_time, l, mean, sd):
        time = 0
        count = 1
        while True:
            exp_time = exponential(l)
            norm_time = normal(mean, sd)
            if time + exp_time + norm_time > max_time:
                break
            self.env.process(self.piece(f'Piece {count}', time + exp_time, norm_time))
            time += exp_time
            count += 1

    def build_simulation_by_pieces(self, max_pieces, l, mean, sd):
        time = 0
        count = 1
        while count <= max_pieces:
            exp_time = exponential(l)
            norm_time = normal(mean, sd)
            self.env.process(self.piece(f'Piece {count}', time + exp_time, norm_time))
            time += exp_time
            count += 1


def main():
    servers = 1
    max_time = 10000
    max_pieces = 1200
    env = simpy.Environment()
    bcs = simpy.Resource(env, capacity=servers)
    p_line = ProductionLine(env, bcs)
    # p_line.build_simulation_by_time(max_time, 5, 4, 0.5)
    p_line.build_simulation_by_pieces(max_pieces, 5, 4, 0.5)
    env.run()

    times = p_line.inspection_times
    y = [average(times[:index + 1]) for index in range(len(times))]

    plt.title("Simulation behavior")
    plt.xlabel("Piece number")
    plt.ylabel("Average time in inspection")
    plt.plot(y, color="red")
    plt.legend(
        [f"servers = {servers}, max time = {max_time}"], loc="upper right")
    txt = 'graphs/' + str(servers) + '_servers.png' if servers > 1 else 'graphs/' + str(servers) + '_server.png'
    plt.savefig(txt)


if __name__ == "__main__":
    main()
