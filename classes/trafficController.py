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
        self.avgDistribution = len(cars) / lanes
        self.emptyLaneSpaces = dict()
        self.occupiedLaneSpaces = dict()
        self.maxCarsInTrafficLane = 0

        # Construct lanes
        for lane in range(0, lanes):
            self.traffic.append({"cars": [], "totalCars": 0})

        # Assign cars to lanes
        for car in cars:
            currentLane = self.traffic[car.currentLane]

            currentLane["cars"].append(car)
            currentLane["totalCars"] += 1

            car.laneOrder = len(currentLane["cars"]) - 1

        # Get number of cars in each lane
        for lane in self.traffic:
            if lane["totalCars"] > self.maxCarsInTrafficLane:
                self.maxCarsInTrafficLane = lane["totalCars"]

            self.carsInEachLane.append(lane["totalCars"])

        # self.carsInEachLane = [8, 11, 9, 5, 7]
        # self.maxCarsInTrafficLane = 11

        for lane in range(0, len(self.carsInEachLane)):
            carsInLane = self.carsInEachLane[lane]
            self.emptyLaneSpaces[lane] = list(
                range(carsInLane, self.maxCarsInTrafficLane)
            )
            self.occupiedLaneSpaces[lane] = list(range(0, carsInLane))

        # self.carsInEachLane = [4, 5, 10, 5]
        # self.carsInEachLane = [8, 14, 7, 7]
        # self.carsInEachLane = [5, 8, 4, 7]
        # self.carsInEachLane = [7, 8, 4, 5]
        # self.carsInEachLane = [7, 3, 7, 7]
        # self.carsInEachLane: [9, 9, 4, 9, 9] interesting case

    ############## PROPERTIES ##############

    @property
    def laneClosure(self):
        return self._laneClosure

    @laneClosure.setter
    def laneClosure(self, value):
        self._laneClosure = value

    ############## METHODS ##############

    def getDiffFromAvg(self, cars, avg):
        diffFromAvg = []

        for num in cars:
            # may need to be diff = num - math.floor(avg)
            diff = num - math.ceil(avg)
            diffFromAvg.append(diff)

        return diffFromAvg

    def getVerticalAdjustmentData(
        newLaneOccupiedSpaces,
        newLaneEmptySpaces,
        currentLaneOccupiedSpaces,
        currentLaneEmptySpaces,
        carsToChangeLanes,
    ):
        verticalAdjustmentData = {}

        newIdx = newLaneOccupiedSpaces.index(
            currentLaneOccupiedSpaces[-carsToChangeLanes]
        )

        newSpacesToAdjust = newLaneOccupiedSpaces[newIdx + 1 :]

        copiedNewLaneOccupiedSpaces = newLaneOccupiedSpaces[:]

        laneOrderRange = currentLaneOccupiedSpaces[-carsToChangeLanes:]

        currentLaneEmptySpaces[0:0] = laneOrderRange
        del currentLaneOccupiedSpaces[-carsToChangeLanes:]

        for space in range(0, len(copiedNewLaneOccupiedSpaces)):
            newLanePosition = space + carsToChangeLanes

            if space in newSpacesToAdjust:
                if newLanePosition in newLaneEmptySpaces:
                    newEmptySpaceIdx = newLaneEmptySpaces.index(newLanePosition)
                    del newLaneEmptySpaces[newEmptySpaceIdx]

                if newLanePosition not in newLaneOccupiedSpaces:
                    newLaneOccupiedSpaces.append(newLanePosition)

        correctedNewLaneConfig = newLaneOccupiedSpaces[:]

        for space in laneOrderRange:
            if space in correctedNewLaneConfig:
                spaceToDelIdx = correctedNewLaneConfig.index(space)
                del correctedNewLaneConfig[spaceToDelIdx]

        verticalAdjustmentData["verticallyAdjustedLane"] = correctedNewLaneConfig
        verticalAdjustmentData["laneOrderRange"] = laneOrderRange

        return verticalAdjustmentData

    def getNewLaneOrderData(
        self,
        occupiedLaneSpaces,
        emptyLaneSpaces,
        currentLane,
        newLane,
        carsToChangeLanes,
    ):
        laneOrderRange = []
        newLaneEmptySpaces = emptyLaneSpaces[newLane]
        newLaneOccupiedSpaces = occupiedLaneSpaces[newLane]
        currentLaneEmptySpaces = emptyLaneSpaces[currentLane]
        currentLaneOccupiedSpaces = occupiedLaneSpaces[currentLane]
        newLaneOrderData = {"laneOrderRange": None, "verticallyAdjustedLane": None}

        # Think really hard about how to make this more performant
        # i.e somehow do this without looping since we're already in a loop
        copiedCurrentLaneOccupiedSpaces = currentLaneOccupiedSpaces[:]

        for occupiedSpace in copiedCurrentLaneOccupiedSpaces:
            if len(laneOrderRange) == carsToChangeLanes:
                break
            elif occupiedSpace in newLaneEmptySpaces:
                laneOrderRange.append(occupiedSpace)
                emptyNewLaneSpaceIndex = newLaneEmptySpaces.index(occupiedSpace)
                currentLaneOccupiedSpaceIndex = currentLaneOccupiedSpaces.index(
                    occupiedSpace
                )

                # Remove occupied space from current lane, add it as empty space
                # in current lane
                del currentLaneOccupiedSpaces[currentLaneOccupiedSpaceIndex]
                currentLaneEmptySpaces.append(occupiedSpace)

                # Remove empty space from new lane, add it as occupied space
                # in new lane
                del newLaneEmptySpaces[emptyNewLaneSpaceIndex]
                newLaneOccupiedSpaces.append(occupiedSpace)

        newLaneOrderData["laneOrderRange"] = laneOrderRange

        print("newLaneOccupiedSpaces", newLaneOccupiedSpaces)
        print("currentLaneOccupiedSpaces", currentLaneOccupiedSpaces)
        print("laneOrderRange", laneOrderRange)

        # This condition needs to be thought through, inaccurate at times
        if len(newLaneOccupiedSpaces) > len(currentLaneOccupiedSpaces) and not len(
            laneOrderRange
        ):
            newLaneOrderData = TrafficController.getVerticalAdjustmentData(
                newLaneOccupiedSpaces,
                newLaneEmptySpaces,
                currentLaneOccupiedSpaces,
                currentLaneEmptySpaces,
                carsToChangeLanes,
            )

        return newLaneOrderData

    def addInstruction(
        self,
        newDiffs,
        firstLaneIdx,
        secondLaneIdx,
        emptyLaneSpaces,
        occupiedLaneSpaces,
        executionOrder,
    ):
        laneChangeInstruction = None
        print("newDiffs", newDiffs)
        carsToChangeLanes = abs(newDiffs[firstLaneIdx])

        currentLane, newLane = (
            (secondLaneIdx, firstLaneIdx)
            if newDiffs[firstLaneIdx] < 0
            else (firstLaneIdx, secondLaneIdx)
        )

        if carsToChangeLanes:
            newLaneOrderData = self.getNewLaneOrderData(
                occupiedLaneSpaces,
                emptyLaneSpaces,
                currentLane,
                newLane,
                carsToChangeLanes,
            )

            if len(newLaneOrderData["laneOrderRange"]):
                laneChangeInstruction = {
                    "currentLane": currentLane,
                    "newLane": newLane,
                    "carsToChangeLanes": carsToChangeLanes,
                    "laneOrderRange": newLaneOrderData["laneOrderRange"],
                    "verticallyAdjustedLane": newLaneOrderData[
                        "verticallyAdjustedLane"
                    ],
                    "executionOrder": executionOrder,
                }

        return laneChangeInstruction

    def setInstructions(
        self, avg, diffsFromAvg, laneClosure, emptyLaneSpaces, occupiedLaneSpaces
    ):
        newDiffs = diffsFromAvg[:]

        # Initially start from both ends i.e move right from
        # left end of array, and move left from right end of
        # array
        moveRight = True
        moveLeft = True

        instructions = []

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

            # ******************** FOR DISPLAY PURPOSES ONLY ********************
            max_spaces = max(max(spaces) for spaces in occupiedLaneSpaces.values()) + 1

            print("\n")
            if instructionsLength == 0:
                print("********** Initial State **********")
            else:
                print(f"********** Instruction {executionOrder} **********")

            # Loop over each lane in the dictionary
            for lane, positions in occupiedLaneSpaces.items():
                # Create a list of '.' representing unoccupied spaces for this lane
                display = ["⬜"] * max_spaces

                # Place a '🚗' at each occupied position
                for pos in positions:
                    display[pos] = "🚗"

                # Print the visual representation of the lane
                print(f"Lane {lane}: " + " ".join(display))

            print("\n")

            # ******************** END DISPLAY OF TRAFFIC ********************

            print("occupiedLaneSpaces", occupiedLaneSpaces)
            print("emptyLaneSpaces", emptyLaneSpaces)
            # If all pointer values are zero, we want to break to avoid adding
            # any unnecessary instructions. Find a better way of breaking, there may
            # be an edge case where all of these are equal but the algo isn't done yet
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

            # TODO: Fix corresponding laneClosure movements, look at case for cars = [24, 11, 0, 0]
            # Also becomes a problem when evaluating for cases with less than 4 lanes
            if secondRightIdx in (firstLeftIdx, secondLeftIdx):
                if laneClosure == "left":
                    moveLeft = False
                elif laneClosure == "right":
                    moveRight = False
                elif laneClosure is None and moveRight and moveLeft:
                    moveLeft = False
            # TODO: Since all lane changes happen concurently, with the exception of the
            # neighboring positives case, need to fix assignment of execution order.
            # In all cases but the above mentioned, the execution order should always be 1

            newInstructionData = {
                "newDiffs": newDiffs,
                "emptyLaneSpaces": emptyLaneSpaces,
                "occupiedLaneSpaces": occupiedLaneSpaces,
                "executionOrder": executionOrder,
            }

            if moveRight:
                newInstructionData["firstLaneIdx"] = firstLeftIdx
                newInstructionData["secondLaneIdx"] = secondLeftIdx

                self.addInstructionAndMove(instructions, newInstructionData, firstLeft)

            if moveLeft:
                newInstructionData["firstLaneIdx"] = firstRightIdx
                newInstructionData["secondLaneIdx"] = secondRightIdx

                self.addInstructionAndMove(instructions, newInstructionData, firstRight)

            # There are cases where no instructions are set, so we should
            # not increment the execution order here
            # Ex. [0, -3, 3, 0] --> On first loop, neither end has a lane change
            if len(instructions) > instructionsLength:
                executionOrder += 1

        return instructions

    def addInstructionAndMove(self, instructions, newInstructionData, carsToMove):
        instruction = self.addInstruction(**newInstructionData)

        if instruction:
            instructions.append(instruction)

            newDiffs = newInstructionData["newDiffs"]
            secondLaneIdx = newInstructionData["secondLaneIdx"]
            firstLaneIdx = newInstructionData["firstLaneIdx"]

            newDiffs[secondLaneIdx] += carsToMove
            newDiffs[firstLaneIdx] += -carsToMove

    def setNewLanes(traffic, instructions):
        totalIterations = sum(
            instruction["carsToChangeLanes"] for instruction in instructions
        )
        carsToMove = []
        increment = 1
        j = 0

        for i in range(0, totalIterations):
            if increment > instructions[j]["carsToChangeLanes"]:
                increment = 1
                j += 1

            currentLane = instructions[j]["currentLane"] - 1

            cars = traffic[currentLane]["cars"]

            cars[increment - 1].newLane = instructions[j]["newLane"]
            cars[increment - 1].executionOrder = instructions[j]["executionOrder"]

            carsToMove.append(cars[increment - 1])

            increment += 1

        return carsToMove
