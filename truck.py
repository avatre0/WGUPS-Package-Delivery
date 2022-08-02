class Truck:

    def __init__(self, name, location, capacity=16, speed=18):
        self.name = name
        self.location = location
        self.capacity = [None] * capacity
        self.speed = speed
