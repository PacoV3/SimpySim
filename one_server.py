import numpy as np
import simpy

time_per_car = []
def car(env, name, bcs, driving_time, charge_duration):
    # Simulate driving to the BCS
    yield env.timeout(driving_time)
    # Request one of its charging spots
    # print('%s arriving at %d' % (name, env.now))

    with bcs.request() as req:
        yield req

        # Charge the battery
        # print('%s starting to charge at %s' % (name, env.now))
        yield env.timeout(charge_duration)
        # print('%s leaving the bcs at %s' % (name, env.now))
        time_per_car.append((name, env.now - driving_time))

env = simpy.Environment()
bcs = simpy.Resource(env, capacity=1)

time = 0
count = 0
max_time = 200
while True:
    exp_time = int(np.random.exponential(5))
    norm_time = int(np.random.normal(4,0.5))
    if time + exp_time + norm_time > max_time:
        break
    # revisar si me pase del 40
    env.process(car(env, 'Car %d' % count, bcs, time + exp_time, norm_time))
    time += exp_time
    count += 1

# for i in range(4):
#     arrive_time = np.random.exponential(5)
#     charge_time = np.random.normal(4,0.5)
#     env.process(car(env, 'Car %d' % i, bcs, arrive_time, charge_time))
#     print(arrive_time, charge_time)

env.run()
sum_of_times = 0
for car, time in time_per_car:
    sum_of_times += time
    # print(f"Average time: {sum_of_times / len(time_per_car)}")
    print(f"Time for {car}: {time}")

