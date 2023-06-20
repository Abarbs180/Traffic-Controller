class TrafficController:

    def __init__(self, lanes, cars):
        self.traffic = []
        self.total_cars = len(cars)
        self.lanes = lanes
        self.cars = cars

        for lane in range(1, lanes+1):
            self.traffic.append(
                {
                    "cars": [],
                    "total_cars": 0
                }
            )

        for car in cars:
            lane_index = car.current_lane - 1

            current_lane = self.traffic[lane_index]
            total_cars_in_lane = self.traffic[lane_index]

            current_lane['cars'].append(car)
            total_cars_in_lane['total_cars'] += 1

            car.lane_order = len(current_lane['cars'])
