from numpy.random import exponential, normal, uniform
import matplotlib.pyplot as plt
import simpy


class ProductionLine:
    def __init__(self, env, grinding, press, cleaning, packing):
        self.env = env
        # Process for gears
        self.grinding = grinding
        # Process for plates
        self.press = press
        # Process for cleaning the pieces
        self.cleaning = cleaning
        # Process for packing
        self.packing = packing
        # Time in the system for gears
        self.gear_times = []
        self.out_gears = 0
        self.plate_times = []
        self.out_plates = 0
        

    # Gear 
    # in_time = Normal(13,2)
    # prod_time = Uniform(1,3)
    # packing_time = Uniform(1,5)
    def gear(self, name, in_time, prod_time, packing_time, transport_time_1, transport_time_2):
        yield self.env.timeout(in_time)
        # print(f"In time for {name}: {self.env.now}")
        if len(self.grinding.queue) <= 30:
            with self.grinding.request() as grinding_req:
                yield grinding_req
                yield self.env.timeout(prod_time)
                # print(f"End of production time for {name}: {self.env.now}")
                yield self.env.timeout(transport_time_1)

                with self.cleaning.request() as cleaning_req:
                    yield cleaning_req
                    yield self.env.timeout(10)
                    yield self.env.timeout(transport_time_2)

                    with self.packing.request() as packing_req:
                        yield packing_req
                        yield self.env.timeout(packing_time)
                        # print(f"End of packing for {name}: {self.env.now}")
                        self.gear_times.append(self.env.now - in_time)
        else:
            self.out_gears += 1


    # Plate 
    # in_time = Exponential(12)
    # prod_time = Exponential(3)
    # packing_time = Uniform(2,7)
    def plate(self, name, in_time, prod_time, packing_time, transport_time_1, transport_time_2):
        yield self.env.timeout(in_time)
        # print(f"In time for {name}: {self.env.now}")
        if len(self.press.queue) <= 30:
            with self.press.request() as press_req:
                yield press_req
                yield self.env.timeout(prod_time)
                # print(f"End of production time for {name}: {self.env.now}")
                yield self.env.timeout(transport_time_1)

                with self.cleaning.request() as cleaning_req:
                    yield cleaning_req
                    yield self.env.timeout(10)
                    yield self.env.timeout(transport_time_2)

                    with self.packing.request() as packing_req:
                        yield packing_req
                        yield self.env.timeout(packing_time)
                        # print(f"End of packing for {name}: {self.env.now}")
                        self.plate_times.append(self.env.now - in_time)
        else:
            self.out_plates += 1


    def build_simulation(self, max_time):
        time = 0
        count = 0
        while True:
            # Random times
            in_time = normal(13,2)
            prod_time = uniform(1,3)
            packing_time = uniform(1,5)
            transport_time_1 = exponential(3)
            transport_time_2 = exponential(3)
            # if the time exceeds the max time
            if time + in_time + prod_time + 10 + transport_time_1 + packing_time + transport_time_2 > max_time:
                # Stop the simulation
                break
            self.env.process(self.gear(f'Gear #{count}', time + in_time, prod_time, packing_time, transport_time_1, transport_time_2))
            time += in_time
            count += 1
        time = 0
        count = 0
        while True:
            # Random times
            in_time = exponential(12)
            prod_time = exponential(3)
            packing_time = uniform(2,7)
            transport_time_1 = exponential(3)
            transport_time_2 = exponential(3)
            # if the time exceeds the max time
            if time + in_time + prod_time + 10 + transport_time_1 + packing_time + transport_time_2 > max_time:
                # Stop the simulation
                break
            self.env.process(self.plate(f'Plate #{count}', time + in_time, prod_time, packing_time, transport_time_1, transport_time_2))
            time += in_time
            count += 1


def main():
    # Definition of the enviroment ( the everything )
    max_time = 19200
    env = simpy.Environment()
    
    # Definition of resources ( the machines/people that work )
    grinding = simpy.Resource(env, capacity=1)
    press = simpy.Resource(env, capacity=1)
    cleaning = simpy.Resource(env, capacity=2)
    packing = simpy.Resource(env, capacity=2)
    
    # Definition of the Production Line
    p_line = ProductionLine(env, grinding, press, cleaning, packing)
    p_line.build_simulation(max_time=max_time)
    env.run()

    gear_times = p_line.gear_times
    plate_times = p_line.plate_times
    y_gear = [sum(gear_times[:index + 1]) / (index + 1) for index in range(len(gear_times))]
    y_plate = [sum(plate_times[:index + 1]) / (index + 1) for index in range(len(plate_times))]

    print(p_line.out_gears, p_line.out_plates)
    print(len(gear_times), len(plate_times))

    plt.title("Simulation behavior")
    plt.xlabel("Piece number")
    plt.ylabel("Average time in inspection")
    plt.plot(y_gear, color="red")
    plt.plot(y_plate, color="blue")
    plt.legend(["Gears", "Plates"])
    txt = 'graphs/multi_process.png'
    plt.savefig(txt)


if __name__ == "__main__":
    main()
