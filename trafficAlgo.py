from classes.car import Car
from classes.traffic_controller import TrafficController
import random

cars = []

# Will eventually read-in cars and lanes, for now just assign at random
for i in range(36):
    new_car = Car()
    new_car.current_lane = random.randint(1, 6)
    cars.append(new_car)

tc = TrafficController(6, cars)

# Will also be read-in
tc.lane_closure = 'right'

print(f'cars_in_each_lane: {tc.cars_in_each_lane}')
print(f'total_cars: {tc.total_cars}')
print(f'avg_distribution: {tc.avg_distribution}')

diffs_from_avg = TrafficController.get_diff_from_avg(
    tc.cars_in_each_lane, tc.avg_distribution)

lane_change_instructions = TrafficController.set_instructions(
    tc.avg_distribution, diffs_from_avg, tc.lane_closure)

new_distribution = TrafficController.set_new_lanes(
    tc.traffic, lane_change_instructions)

# for i in range(0, len(new_distribution)):
#     print(f'car number {i+1}')
#     print(f'current lane: {new_distribution[i].current_lane}')
#     print(f'new lane: {new_distribution[i].new_lane}')
#     print(f'lane order: {new_distribution[i].lane_order}')
#     print(f'execution order: {new_distribution[i].execution_order}')
#     print('*******************************************')


# For testing purposes only :)
print('\n')
print('**** INSTRUCTIONS ****')
print('\n')
for i in range(0, len(lane_change_instructions)):
    print(lane_change_instructions[i])
    print('\n')
