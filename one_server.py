import numpy as np
import simpy

def car(env, name, bcs, driving_time, charge_duration):
    # Simulate driving to the BCS
    yield env.timeout(driving_time)
    # Request one of its charging spots
    print('%s arriving at %d' % (name, env.now))

    with bcs.request() as req:
        yield req

        # Charge the battery
        print('%s starting to charge at %s' % (name, env.now))
        yield env.timeout(charge_duration)
        print('%s leaving the bcs at %s' % (name, env.now))

env = simpy.Environment()
bcs = simpy.Resource(env, capacity=2)

# time = 0
# count = 0
# while time < 120:
#     dist = dist_exp(5)
#     # revisar si me pase del 40
#     env.process(car(env, 'Car %d' % count, bcs, time + dist, 5))
#     count += 1
#     time += dist

for i in range(4):
    arrive_time = np.random.exponential(5)
    charge_time = np.random.normal(4,0.5)
    env.process(car(env, 'Car %d' % i, bcs, arrive_time, charge_time))
    print(arrive_time, charge_time)

env.run()
