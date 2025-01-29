from classes.car import Car
from classes.trafficController import TrafficController
import random

cars = []

# Will eventually read-in cars and lanes, for now just assign at random
for i in range(40):
    newCar = Car()
    newCar.currentLane = random.randint(0, 4)
    cars.append(newCar)

tc = TrafficController(5, cars)

# Will also be read-in
tc.laneClosure = None

print(f"carsInEachLane: {tc.carsInEachLane}")
print(f"totalCars: {tc.totalCars}")
print(f"avgDistribution: {tc.avgDistribution}")

diffsFromAvg = tc.getDiffFromAvg(tc.carsInEachLane, tc.avgDistribution)

laneChangeInstructions = tc.setInstructions(
    tc.avgDistribution,
    diffsFromAvg,
    tc.laneClosure,
    tc.emptyLaneSpaces,
    tc.occupiedLaneSpaces,
)

# newDistribution = TrafficController.setNewLanes(
#     tc.traffic, laneChangeInstructions)

# For testing purposes only :)
print("\n")
print("**** INSTRUCTIONS ****")
print("\n")
for i in range(0, len(laneChangeInstructions)):
    print(laneChangeInstructions[i])
    print("\n")
