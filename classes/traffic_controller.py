import math
from collections import OrderedDict

class TrafficController:

    # Make 'lane_closure' a property here
    def __init__(self, lanes, cars):
        self.traffic = []
        self.cars_in_each_lane = []
        self.total_cars = len(cars)
        self.lanes = lanes
        self.cars = cars
        self.avg_distribution = int(len(cars) / lanes)

        # Construct lanes
        for lane in range(1, lanes+1):
            self.traffic.append(
                {
                    "cars": [],
                    "total_cars": 0
                }
            )

        # Assign cars to lanes
        for car in cars:
            lane_index = car.current_lane - 1

            current_lane = self.traffic[lane_index]

            current_lane['cars'].append(car)
            current_lane['total_cars'] += 1

            car.lane_order = len(current_lane['cars'])

        # Get number of cars in each lane
        for lane in self.traffic:
            self.cars_in_each_lane.append(lane['total_cars'])

    ############## PROPERTIES ##############

    @property
    def lane_closure(self):
        return self._lane_closure

    @lane_closure.setter
    def lane_closure(self, value):
        self._lane_closure = value

    ############## METHODS ##############

    def get_diff_from_avg(cars, avg):
        diff_from_avg = []
        for num in cars:
            diff = num - math.floor(avg)
            diff_from_avg.append(diff)
        return diff_from_avg

    def add_instruction(first_lane_idx, second_lane_idx, first_lane_cars, second_lane_cars, first_lane_diff, empty_lane_spaces, execution_order):
        lane_change_instruction = None

        # If negative, move cars from second lane to first
        if first_lane_diff < 0:
            if second_lane_idx in empty_lane_spaces:
                lane_order_start = empty_lane_spaces[first_lane_idx][0]
                lane_order_end = lane_order_start + abs(first_lane_diff)
            else:
                lane_order_start = first_lane_cars + 1
                lane_order_end = first_lane_cars + abs(first_lane_diff)
                
            lane_order_range = list(range(lane_order_start, lane_order_end + 1))

            lane_change_instruction = {
                'current_lane': second_lane_idx,
                'new_lane': first_lane_idx,
                'cars_to_change_lanes': abs(first_lane_diff),
                'lane_order_range': lane_order_range,
                'execution_order': execution_order
            }
            
        # If positive, move cars from first lane to second
        elif first_lane_diff > 0:
            if first_lane_idx in empty_lane_spaces:
                lane_order_start = empty_lane_spaces[second_lane_idx][0]
                lane_order_end = lane_order_start + abs(first_lane_diff)
            else:
                lane_order_start = second_lane_cars + 1
                lane_order_end = second_lane_cars + first_lane_diff
            
            lane_order_range = list(range(lane_order_start, lane_order_end + 1))
            
            lane_change_instruction = {
                'current_lane': first_lane_idx,
                'new_lane': second_lane_idx,
                'cars_to_change_lanes': abs(first_lane_diff),
                'lane_order_range': lane_order_range,
                'execution_order': execution_order
            }

        return lane_change_instruction

    def set_instructions(avg, diffs_from_avg, lane_closure):
        print('\n')
        print(f'diffs_from_avg: {diffs_from_avg}')
        new_diffs = diffs_from_avg[:]

        # Initially start from both ends i.e move right from
        # left end of array, and move left from right end of
        # array
        move_right = True
        move_left = True

        instructions = []
        empty_lane_spaces = dict()

        # Determines the order of executed instructions
        execution_order = 1

        for i in range(1, len(new_diffs)):
            first_left_idx = i - 1
            second_left_idx = i
            first_left = new_diffs[first_left_idx]
            second_left = new_diffs[second_left_idx]

            first_right_idx = len(new_diffs) - i
            second_right_idx = len(new_diffs) - (i + 1)
            first_right = new_diffs[first_right_idx]
            second_right = new_diffs[second_right_idx]

            instructions_length = len(instructions)

            # If all pointer values are zero, we want to break to avoid adding
            # any unnecessary instructions
            if first_left == second_left == first_right == second_right:
                break

            # If either the left or right two pointers combine to be
            # less than the negative of the average, then it does
            # not make sense to make lane changes in that direction
            # Ex. avg = 9, [-5, -5, 5, 5] --> move_right = False
            if first_left + second_left < -avg:
                move_right = False

            if first_right + second_right < -avg:
                move_left = False

            # TODO: Include case for two neighboring positives, we are currently
            # just adding them together into the same lane, but this is not optimal,
            # should instead be moving both positives to new lanes concurrently

            # Fix corresponding lane_closure movements, look at case for cars = [24, 11, 0, 0]
            # Also becomes a problem when evaluating for cases with less than 4 lanes
            if second_right_idx in (first_left_idx, second_left_idx):
                if lane_closure == 'left':
                    move_left = False
                elif lane_closure == 'right':
                    move_right = False
                elif lane_closure == None and (move_right and move_left):
                    move_left = False
            # TODO: Since all lane changes happen concurently, with the exception of the 
            # neighboring positives case, need to fix assignment of execution order.
            # In all cases but the above mentioned, the execution order should always be 1
            if move_right:

                first_left_cars = avg + new_diffs[first_left_idx]
                second_left_cars = avg + new_diffs[second_left_idx]

                instruction = TrafficController.add_instruction(
                    first_left_idx + 1, second_left_idx + 1, first_left_cars, second_left_cars, first_left, empty_lane_spaces, execution_order)
                
                if instruction:
                    instructions.append(instruction)
                    empty_lane_spaces[instruction['current_lane']] = instruction['lane_order_range']

                new_diffs[second_left_idx] += first_left
                new_diffs[first_left_idx] += -first_left

            if move_left:

                first_right_cars = avg + new_diffs[first_right_idx]
                second_right_cars = avg + new_diffs[second_right_idx]

                instruction = TrafficController.add_instruction( 
                    first_right_idx + 1, second_right_idx + 1, first_right_cars, second_right_cars, first_right, empty_lane_spaces, execution_order)
                
                if instruction:
                    instructions.append(instruction)
                    empty_lane_spaces[instruction['current_lane']] = instruction['lane_order_range']

                new_diffs[second_right_idx] += first_right
                new_diffs[first_right_idx] += -first_right

            print(empty_lane_spaces)

            print('\n')
            print(f'diffs_from_avg: {new_diffs}')

            # There are cases where no instructions are set, so we should
            # not increment the execution order here
            # Ex. [0, -3, 3, 0] --> On first loop, neither end has a lane change
            if len(instructions) > instructions_length:
                execution_order += 1

        return instructions

    def set_new_lanes(traffic, instructions):
        total_iterations = sum(instruction['cars_to_change_lanes'] for instruction in instructions)
        cars_to_move = []
        increment = 1
        j = 0

        for i in range(0, total_iterations):
            if increment > instructions[j]['cars_to_change_lanes']:
                increment = 1
                j += 1

            current_lane = instructions[j]['current_lane'] - 1

            cars = traffic[current_lane]['cars']

            cars[increment - 1].new_lane = instructions[j]['new_lane']
            cars[increment - 1].execution_order = instructions[j]['execution_order']

            cars_to_move.append(cars[increment - 1])

            increment += 1

        return cars_to_move
