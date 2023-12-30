from classes.car import Car
from classes.trafficController import TrafficController
import random

cars = []

# Will eventually read-in cars and lanes, for now just assign at random
for i in range(24):
    newCar = Car()
    newCar.currentLane = random.randint(0, 3)
    cars.append(newCar)

tc = TrafficController(4, cars)

# Will also be read-in
tc.laneClosure = None

print(f'carsInEachLane: {tc.carsInEachLane}')
print(f'totalCars: {tc.totalCars}')
print(f'avgDistribution: {tc.avgDistribution}')

diffsFromAvg = TrafficController.getDiffFromAvg(
    tc.carsInEachLane, tc.avgDistribution)

laneChangeInstructions = TrafficController.setInstructions(
    tc.avgDistribution, diffsFromAvg, tc.laneClosure)

# newDistribution = TrafficController.setNewLanes(
#     tc.traffic, laneChangeInstructions)

# for i in range(0, len(newDistribution)):
#     print(f'car number {i+1}')
#     print(f'current lane: {newDistribution[i].currentLane}')
#     print(f'new lane: {newDistribution[i].newLane}')
#     print(f'lane order: {newDistribution[i].laneOrder}')
#     print(f'execution order: {newDistribution[i].executionOrder}')
#     print('*******************************************')


# For testing purposes only :)
print('\n')
print('**** INSTRUCTIONS ****')
print('\n')
for i in range(0, len(laneChangeInstructions)):
    print(laneChangeInstructions[i])
    print('\n')
