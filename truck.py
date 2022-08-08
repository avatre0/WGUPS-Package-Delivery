from datetime import time


class Truck:

    def __init__(self, name, location="4001 South 700 East", speed=18):
        self.name = name
        self.location = location
        self.capacity = []
        self.speed = speed
        self.distance_driven = 0
        self.current_time = time(8, 0, 0)

    def load_package(self, package):
        self.capacity.append(package)

    def package_delivered(self, package):
        self.capacity.remove(package)
