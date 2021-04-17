from numpy.random import exponential
from numpy import average
# import matplotlib.pyplot as plt
import simpy


class ProductionLine:
    def __init__(self, env, bcs, max_time):
        self.env = env
        self.bcs = bcs
        self.max_time = max_time
        self.count = 0
        self.process_time = 0
        self.queue_count_record = []
        self.queue_time_record = []

    def piece(self, piece_type, arriving_time, inspect_time):
        yield self.env.timeout(arriving_time)
        with self.bcs.request() as req:
            self.queue_count_record.append(len(self.bcs.queue))
            start_of_waiting = self.env.now
            yield req
            self.queue_time_record.append(self.env.now - start_of_waiting)
            self.process_time += inspect_time
            yield self.env.timeout(inspect_time)

    def build_simulation(self, times):
        piece_type = 0
        for in_times, out_times in times:
            time = 0
            while True:
                exp_in_time = exponential(in_times)
                exp_out_time = exponential(out_times)
                if time > self.max_time:
                    break
                self.env.process(self.piece(piece_type, time + exp_in_time, exp_out_time))
                time += exp_in_time
                self.count += 1
            piece_type += 1


def main():
    servers = 1
    max_time = 6000
    env = simpy.Environment()
    bcs = simpy.Resource(env, capacity=servers)
    p_line = ProductionLine(env, bcs, max_time)
    p_line.build_simulation(times=[(30,3),(15,5),(30,10)])
    env.run(until=max_time)

    print(f"a) {p_line.process_time / max_time * 100:.4f} %")
    print(f"b) {p_line.count} pieces")
    print(f"d) {average(p_line.queue_time_record):.4f} minutes")
    print(f"d) {average(p_line.queue_count_record):.4f} pieces")

    # times = p_line.all_inspection_times
    # y = [average(times[:index + 1]) for index in range(len(times))]

    # plt.title("Simulation behavior")
    # plt.xlabel("Piece number")
    # plt.ylabel("Average time in inspection")
    # plt.plot(y, color="red")
    # plt.legend(
    #     [f"servers = {servers}, max time = {max_time}"])
    # txt = 'graphs/' + str(servers) + '_servers.png' if servers > 1 else 'graphs/' + str(servers) + '_server.png'
    # plt.savefig(txt)


if __name__ == "__main__":
    main()
