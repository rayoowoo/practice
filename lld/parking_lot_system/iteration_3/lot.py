# thirds iteration will have:
    # dynamic parking lot size
    # track when cars come in and when they exit
    # cars can decide to park on any level
    # all cars can still park in all spots (not tracking individual spots)

from dataclasses import dataclass
from functools import cached_property

@dataclass
class ParkEvent:
    level: int
    license: str
    enter: int
    exit: int = None

    def __post_init__(self):
        print(f"Car {license} entered at {self.enter}")

    def end(self, time: int):        
        self.exit = time
        print(f"Car {license} left at {time}")

@dataclass
class ParkingLot:

    capacity_per_level: int
    levels: int

    def __post_init__(self):
        self.LEVELS = [0] * self.levels
        self.cars_parked = {}

    def car_enters(self, license: str, time: int, level: int):
        if self.cars_parked.get(license):
            print(f"This car {license} is already parked!")
        elif level > self.levels:
            print(f"There is no level above {self.levels}.")
        elif self.LEVELS[level] == self.capacity_per_level:
            print(f"Level {level} of the lot is full.")
        else:
            self.LEVELS[level] += 1
            self.cars_parked[license] = ParkEvent(level, license, time)
            return True
        
        return False
    
    def car_leaves(self, license: str, time: int):
        car = self.cars_parked.get(license)
        if not car:
            print(f"This car {license} has not parked here.")
        elif car.enter > time:
            print(f"This car {license} cannot be leaving before it entered.")
        elif car.exit:
            print(f"This car {license} has already left the lot at {car.exit}")
        else:        
            car.end(time)
            self.LEVELS[car.level] -= 1
            return True
    
        return False
    
    def is_lot_full(self):
        return self.capacity == 0
    
    @property
    def capacity(self):
        return self.total_capacity - sum(self.LEVELS)
    
    @cached_property
    def total_capacity(self):
        return self.capacity_per_level * self.levels
            