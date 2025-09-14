# thirds iteration will have:
    # dynamic parking lot size
    # track when cars come in and when they exit
    # cars can decide to park on any level
    # compact spots can take cars size 1 or 2, and regular spots can take sizes 1-4

from dataclasses import dataclass
from functools import cached_property

@dataclass
class Car:
    license: str
    size: int

    @property
    def is_compact(self):
        return self.size <= 2

@dataclass
class ParkingLotLevel:
    capacity: int
    num: int
    
    def __post_init__(self):
        self.compact_capacity = int(self.capacity // 2)
        self.regular_capacity = self.capacity - self.compact_capacity

        self.compact_spots_filled = 0
        self.regular_spots_filled = 0

        self.cars_parked = {}

    @property
    def open_spaces(self):
        return self.capacity - self.compact_spots_filled - self.regular_spots_filled
    
    @property
    def open_regular_spaces(self):
        return self.regular_capacity - self.regular_spots_filled
    
    @property
    def is_full(self):
        return self.open_spaces == 0
    
    def car_enters(self, car: Car, time: int):
        if self.cars_parked.get(car.license):
            print(f"This car {car.license} is already parked!")
            return False
        elif car.is_compact:
            return self._handle_compact_car(car, time)
        else:
            return self._handle_regular_car(car, time)
        
    def _handle_compact_car(self, car, time):
        if not self.open_spaces:
            print(f"This level of the lot is full.")
            return False
        else:
            if self.compact_spots_filled < self.compact_capacity:
                self.compact_spots_filled += 1
                compact_spot = True
            else:
                self.regular_spots_filled += 1
                compact_spot = False
            self.cars_parked[car.license] = ParkEvent(car, time, compact_spot)

            return True
    
    def _handle_regular_car(self, car, time):
        if not self.open_regular_spaces:
            print(f"This level of the lot is full for regular-sized cars.")
            return False
        else:
            self.cars_parked[car.license] = ParkEvent(car, time, False)
            self.regular_spots_filled += 1
            return True
        
    def car_leaves(self, car: Car, time: int):
        park_event: ParkEvent = self.cars_parked.get(car.license)
        if not park_event:
            print(f"This car {car.license} has not parked here.")
        elif park_event.enter > time:
            print(f"This car {car.license} cannot be leaving before it entered.")
        elif park_event.exit:
            print(f"This car {car.license} has already left the lot at {park_event.exit}.")
        else:  
            park_event.end(time)
        
            if park_event.compact_spot:
                self.compact_spots_filled -= 1
            else:
                self.regular_spots_filled -= 1

            return True

        return False          


@dataclass
class ParkEvent:
    car: Car
    enter: int
    compact_spot: bool
    exit: int = None

    def __post_init__(self):
        print(f"Car {self.car.license} entered at {self.enter}.")

    def end(self, time: int):        
        self.exit = time
        print(f"Car {self.car.license} left at {time}.")

@dataclass
class ParkingLot:

    capacity_per_level: int
    levels: int

    def __post_init__(self):
        self.LEVELS = []
        for i in range(self.levels):
            self.LEVELS.append(ParkingLotLevel(self.capacity_per_level, i))
        self.cars_parked = {}

    def car_enters(self, car: Car, time: int, level_num: int):
        level = self.LEVELS[level_num]
        parked = level.car_enters(car, time)
        if parked:
            self.cars_parked[car.license] = level
            return True
        
        return False
    
    def car_leaves(self, car: Car, time: int):
        level: ParkingLotLevel = self.cars_parked[car.license]
        leaves = level.car_leaves(car, time)
        return leaves
    
    @property
    def is_lot_full(self):
        return all([level.is_full for level in self.LEVELS])
    
    @property
    def capacity(self):
        return sum([level.open_spaces for level in self.LEVELS])
    
    @cached_property
    def total_capacity(self):
        return self.capacity_per_level * self.levels
            