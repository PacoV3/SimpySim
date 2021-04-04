from numpy.random import exponential, normal
import matplotlib.pyplot as plt
import simpy


class ProductionLine:
    def __init__(self, env, bcs, l, mean, sd):
        self.env = env
        self.bcs = bcs
        self.l = l
        self.mean = mean
        self.sd = sd
        self.inspection_times = []

    def piece(self, name, arriving_time, inspect_time):
        # Simulate the piece arriving to the BCS
        yield self.env.timeout(arriving_time)
        # Request one of its inspection spots
        # print('%s arriving at %d' % (name, self.env.now))
        with self.bcs.request() as req:
            yield req
            # Charge the battery
            # print('%s starting to inspect at %s' % (name, self.env.now))
            yield self.env.timeout(inspect_time)
            # print('%s leaving the bcs at %s' % (name, self.env.now))
            self.inspection_times.append(self.env.now - arriving_time)

    def build_simulation(self, max_time):
        time = 0
        count = 0
        while True:
            exp_time = exponential(self.l)
            norm_time = normal(self.mean, self.sd)
            if time + exp_time + norm_time > max_time:
                break
            self.env.process(self.piece('Piece %d' %
                                        count, time + exp_time, norm_time))
            time += exp_time
            count += 1


def main():
    servers = 1
    max_time = 10000
    env = simpy.Environment()
    bcs = simpy.Resource(env, capacity=servers)
    p_line = ProductionLine(env, bcs, 5, 4, 0.5)
    p_line.build_simulation(max_time=max_time)
    env.run()

    times = p_line.inspection_times
    x = range(len(times))
    y = [sum(times[:index + 1]) / (index + 1) for index in range(len(times))]

    plt.title("Simulation behavior")
    plt.xlabel("Piece number")
    plt.ylabel("Average time in inspection")
    plt.plot(x, y, color="red")
    plt.legend(
        [f"servers = {servers}, max time = {max_time}"], loc="upper right")
    txt = 'graphs/' + str(servers) + '_servers.png' if servers > 1 else 'graphs/' + str(servers) + '_server.png'
    plt.savefig(txt)


if __name__ == "__main__":
    main()
