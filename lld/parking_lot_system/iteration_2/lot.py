# second iteration will have:
    # fixed parking lot size
    # track when cars come in and when they exit
    # cars park in a round-robin order of lot levels
    # all cars can still park in all spots (not tracking individual spots)

from dataclasses import dataclass

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

    capacity_per_level = 100

    LEVELS = [0, 0, 0]
    cars_parked = {}

    def car_enters(self, license: str, time: int):
        if self.cars_parked.get(license):
            print(f"This car {license} is already parked!")
        else:
            for i in range(3):
                if self.LEVELS[i] < self.capacity_per_level:
                    self.LEVELS[i] += 1
                    self.cars_parked[license] = ParkEvent(i, license, time)
                    return True
        
        return False
    
    def car_leaves(self, license: str, time: int):
        car = self.cars_parked.get(license)
        if not car:
            print(f"This car {license} has not parked here.")
            return False
        elif car.enter > time:
            print(f"This car {license} cannot be leaving before it entered.")
            return False
        elif car.exit:
            print(f"This car {license} has already left the lot at {car.exit}")
            return False
        
        car.end(time)
        self.LEVELS[car.level] -= 1
        return True
    
    def is_lot_full(self):
        return all([level == 100 for level in self.LEVELS])
    
    @property
    def capacity(self):
        return 300 - sum(self.LEVELS)
            