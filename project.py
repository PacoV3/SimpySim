from numpy.random import exponential, gamma, uniform
from numpy import average
import simpy


class Simulation:
    def __init__(self, env, office):
        self.env = env
        self.office = office
        self.count = 0
        self.queue_count_record = []
        self.system_time = [[],[]]


    def client(self, client_type, arriving_time, process_time):
        yield self.env.timeout(arriving_time)
        with self.office.request() as req:
            self.queue_count_record.append(len(self.office.queue))
            yield req
            yield self.env.timeout(process_time)
            self.system_time[client_type - 1].append(self.env.now - arriving_time)


    def build_simulation(self):
        client2_count = 0
        client_type = 2
        time = 0
        while client2_count < 500:
            in_time = 120
            process_time = gamma(2, 35 / 2) # Distribucion 2Erlang(35)
            time += in_time
            self.env.process(self.client(client_type, time, process_time)) # Crear cliente tipo 2
            client2_count += 1

        client_type = 1
        max_time = time
        time = 0
        while True:
            in_time = uniform(100, 150)
            process_time = exponential(25)
            time += in_time
            if time > max_time:
                break # Termina el while
            self.env.process(self.client(client_type, time, process_time)) # Crear cliente tipo 1
            self.count += 1


def main():
    servers = 1
    env = simpy.Environment()
    office = simpy.Resource(env, capacity=servers)
    sim = Simulation(env, office)
    sim.build_simulation()
    env.run()

    print(f"a) Total sim time: {env.now}")
    print(f"b) Type 1 clients: {sim.count}")
    print(f"c) Average for client 1: {average(sim.system_time[0])}, Average for client 2: {average(sim.system_time[1])}")
    print(f"d) Max clients: {max(sim.queue_count_record)}")

if __name__ == "__main__":
    main()
