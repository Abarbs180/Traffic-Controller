import math
from collections import OrderedDict

class TrafficController:

    # Make 'laneClosure' a property here
    def __init__(self, lanes, cars):
        self.traffic = []
        self.carsInEachLane = []
        self.totalCars = len(cars)
        self.lanes = lanes
        self.cars = cars
        self.avgDistribution = int(len(cars) / lanes)

        # Construct lanes
        for lane in range(1, lanes+1):
            self.traffic.append(
                {
                    "cars": [],
                    "totalCars": 0
                }
            )

        # Assign cars to lanes
        for car in cars:
            currentLane = self.traffic[car.currentLane]

            currentLane['cars'].append(car)
            currentLane['totalCars'] += 1

            car.laneOrder = len(currentLane['cars']) - 1

        # Get number of cars in each lane
        for lane in self.traffic:
            self.carsInEachLane.append(lane['totalCars'])

    ############## PROPERTIES ##############

    @property
    def laneClosure(self):
        return self._laneClosure

    @laneClosure.setter
    def laneClosure(self, value):
        self._laneClosure = value

    ############## METHODS ##############

    def getDiffFromAvg(cars, avg):
        diffFromAvg = []

        for num in cars:
            diff = num - math.floor(avg)
            diffFromAvg.append(diff)

        return diffFromAvg

    def addInstruction(avg, newDiffs, firstLaneIdx, secondLaneIdx, emptyLaneSpaces, executionOrder):
        laneChangeInstruction = None

        firstLaneDiff = newDiffs[firstLaneIdx]
        firstLaneCars = avg + newDiffs[firstLaneIdx]
        secondLaneCars = avg + newDiffs[secondLaneIdx]

        # If negative, move cars from second lane to first
        if firstLaneDiff < 0:
            currentLane = secondLaneIdx
            newLane = firstLaneIdx

            if secondLaneIdx in emptyLaneSpaces:
                laneOrderStart = emptyLaneSpaces[firstLaneIdx][0]
                laneOrderEnd = laneOrderStart + abs(firstLaneDiff)
            else:
                laneOrderStart = firstLaneCars
                laneOrderEnd = laneOrderStart + abs(firstLaneDiff)
                
            laneOrderRange = list(range(laneOrderStart, laneOrderEnd))

            laneChangeInstruction = {
                'currentLane': currentLane,
                'newLane': newLane,
                'carsToChangeLanes': abs(firstLaneDiff),
                'laneOrderRange': laneOrderRange,
                'executionOrder': executionOrder
            }

        # If positive, move cars from first lane to second
        elif firstLaneDiff > 0:
            currentLane = firstLaneIdx
            newLane = secondLaneIdx

            if firstLaneIdx in emptyLaneSpaces:
                laneOrderStart = emptyLaneSpaces[secondLaneIdx][0]
                laneOrderEnd = laneOrderStart + abs(firstLaneDiff)
            else:
                laneOrderStart = secondLaneCars
                laneOrderEnd = laneOrderStart + firstLaneDiff
            
            laneOrderRange = list(range(laneOrderStart, laneOrderEnd))

            laneChangeInstruction = {
                'currentLane': currentLane,
                'newLane': newLane,
                'carsToChangeLanes': abs(firstLaneDiff),
                'laneOrderRange': laneOrderRange,
                'executionOrder': executionOrder
            }

        return laneChangeInstruction

    def setInstructions(avg, diffsFromAvg, laneClosure):
        print('\n')
        print(f'diffsFromAvg: {diffsFromAvg}')
        newDiffs = diffsFromAvg[:]

        # Initially start from both ends i.e move right from
        # left end of array, and move left from right end of
        # array
        moveRight = True
        moveLeft = True

        instructions = []
        emptyLaneSpaces = dict()

        # Determines the order of executed instructions
        executionOrder = 1

        for i in range(1, len(newDiffs)):
            firstLeftIdx = i - 1
            secondLeftIdx = i
            firstLeft = newDiffs[firstLeftIdx]
            secondLeft = newDiffs[secondLeftIdx]

            firstRightIdx = len(newDiffs) - i
            secondRightIdx = len(newDiffs) - (i + 1)
            firstRight = newDiffs[firstRightIdx]
            secondRight = newDiffs[secondRightIdx]

            instructionsLength = len(instructions)

            # If all pointer values are zero, we want to break to avoid adding
            # any unnecessary instructions
            if firstLeft == secondLeft == firstRight == secondRight:
                break

            # If either the left or right two pointers combine to be
            # less than the negative of the average, then it does
            # not make sense to make lane changes in that direction
            # Ex. avg = 9, [-5, -5, 5, 5] --> moveRight = False
            if firstLeft + secondLeft < -avg:
                moveRight = False

            if firstRight + secondRight < -avg:
                moveLeft = False

            # TODO: Include case for two neighboring positives, we are currently
            # just adding them together into the same lane, but this is not optimal,
            # should instead be moving both positives to new lanes concurrently

            # Fix corresponding laneClosure movements, look at case for cars = [24, 11, 0, 0]
            # Also becomes a problem when evaluating for cases with less than 4 lanes
            if secondRightIdx in (firstLeftIdx, secondLeftIdx):
                if laneClosure == 'left':
                    moveLeft = False
                elif laneClosure == 'right':
                    moveRight = False
                elif laneClosure == None and (moveRight and moveLeft):
                    moveLeft = False
            # TODO: Since all lane changes happen concurently, with the exception of the 
            # neighboring positives case, need to fix assignment of execution order.
            # In all cases but the above mentioned, the execution order should always be 1
            if moveRight:

                instruction = TrafficController.addInstruction(avg, newDiffs, firstLeftIdx, secondLeftIdx, emptyLaneSpaces, executionOrder)
                
                if instruction:
                    instructions.append(instruction)
                    emptyLaneSpaces[instruction['currentLane']] = instruction['laneOrderRange']

                newDiffs[secondLeftIdx] += firstLeft
                newDiffs[firstLeftIdx] += -firstLeft

            if moveLeft:

                instruction = TrafficController.addInstruction(avg, newDiffs, firstRightIdx, secondRightIdx, emptyLaneSpaces, executionOrder)
                
                if instruction:
                    instructions.append(instruction)
                    emptyLaneSpaces[instruction['currentLane']] = instruction['laneOrderRange']

                newDiffs[secondRightIdx] += firstRight
                newDiffs[firstRightIdx] += -firstRight

            print(emptyLaneSpaces)

            print('\n')
            print(f'diffsFromAvg: {newDiffs}')

            # There are cases where no instructions are set, so we should
            # not increment the execution order here
            # Ex. [0, -3, 3, 0] --> On first loop, neither end has a lane change
            if len(instructions) > instructionsLength:
                executionOrder += 1

        return instructions

    def setNewLanes(traffic, instructions):
        totalIterations = sum(instruction['carsToChangeLanes'] for instruction in instructions)
        carsToMove = []
        increment = 1
        j = 0

        for i in range(0, totalIterations):
            if increment > instructions[j]['carsToChangeLanes']:
                increment = 1
                j += 1

            currentLane = instructions[j]['currentLane'] - 1

            cars = traffic[currentLane]['cars']

            cars[increment - 1].newLane = instructions[j]['newLane']
            cars[increment - 1].executionOrder = instructions[j]['executionOrder']

            carsToMove.append(cars[increment - 1])

            increment += 1

        return carsToMove
