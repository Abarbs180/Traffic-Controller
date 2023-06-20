class Car:
    last_id = 0

    def __init__(self):
        self.id = Car.last_id
        Car.last_id += 1

    @property
    def current_lane(self):
        return self._current_lane

    @property
    def lane_order(self):
        return self._lane_order

    @property
    def new_lane(self):
        return self._new_lane

    @current_lane.setter
    def current_lane(self, value):
        self._current_lane = value

    @lane_order.setter
    def lane_order(self, value):
        self._lane_order = value

    @new_lane.setter
    def new_lane(self, value):
        self._new_lane = value
