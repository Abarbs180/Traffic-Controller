import math
from classes.car import Car
from classes.traffic_controller import TrafficController
import random

cars = []

for i in range(36):
    new_car = Car()
    new_car.current_lane = random.randint(1, 6)
    cars.append(new_car)

traffic_controller = TrafficController(6, cars)

cars_in_each_lane = []
for lane in traffic_controller.traffic:
    cars_in_each_lane.append(lane['total_cars'])

print(f'cars_in_each_lane: {cars_in_each_lane}')
print(f'total_cars: {traffic_controller.total_cars}')

avg = traffic_controller.total_cars / traffic_controller.lanes

print(f'avg: {avg}')


def get_diff_from_avg(cars):
    diff_from_avg = []
    for num in cars:
        diff = num - math.floor(avg)
        diff_from_avg.append(diff)
    return diff_from_avg


diffs_from_avg = get_diff_from_avg(cars_in_each_lane)


def add_instruction(first_lane, second_lane, cars_to_change_lanes, execution_order):
    lane_change_instruction = None

    if cars_to_change_lanes < 0:
        lane_change_instruction = {
            'current_lane': second_lane,
            'new_lane': first_lane,
            'cars_to_change_lanes': abs(cars_to_change_lanes),
            'execution_order': execution_order
        }
    elif cars_to_change_lanes > 0:
        lane_change_instruction = {
            'current_lane': first_lane,
            'new_lane': second_lane,
            'cars_to_change_lanes': abs(cars_to_change_lanes),
            'execution_order': execution_order
        }

    return lane_change_instruction


def set_lane_changes(avg, diffs_from_avg, lane_closure):
    print('\n')
    print(f'diffs_from_avg: {diffs_from_avg}')
    new_diffs = diffs_from_avg[:]

    # Initially start from both ends i.e move right from
    # left end of array, and move left from right end of
    # array
    move_right = True
    move_left = True

    instructions = []

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

        if move_right:
            instruction = add_instruction(
                first_left_idx + 1, second_left_idx + 1, first_left, execution_order)

            if instruction:
                instructions.append(instruction)

            new_diffs[second_left_idx] += first_left
            new_diffs[first_left_idx] += -first_left

        if move_left:
            instruction = add_instruction(
                first_right_idx + 1, second_right_idx + 1, first_right, execution_order)

            if instruction:
                instructions.append(instruction)

            new_diffs[second_right_idx] += first_right
            new_diffs[first_right_idx] += -first_right

        print('\n')
        print(f'diffs_from_avg: {new_diffs}')

        # There are cases where no instructions are set, so we should
        # not increment the execution order here
        # Ex. [0, -3, 3, 0] --> On first loop, neither end has a lane change
        if len(instructions) > instructions_length:
            execution_order += 1

    return instructions


lane_change_instructions = set_lane_changes(avg, diffs_from_avg, None)


# For testing purposes only :)
print('\n')
print('**** INSTRUCTIONS ****')
print('\n')
for i in range(0, len(lane_change_instructions)):
    print(lane_change_instructions[i])
    print('\n')
