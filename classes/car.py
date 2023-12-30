class Car:
    lastId = 0

    def __init__(self):
        self.id = Car.lastId
        Car.lastId += 1

    @property
    def currentLane(self):
        return self._currentLane

    @currentLane.setter
    def currentLane(self, value):
        self._currentLane = value

    @property
    def laneOrder(self):
        return self._laneOrder

    @laneOrder.setter
    def laneOrder(self, value):
        self._laneOrder = value

    @property
    def newLane(self):
        return self._newLane

    @newLane.setter
    def newLane(self, value):
        self._newLane = value

    @property
    def executionOrder(self):
        return self._executionOrder

    @executionOrder.setter
    def executionOrder(self, value):
        self._executionOrder = value
