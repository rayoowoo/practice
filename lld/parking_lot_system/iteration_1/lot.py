# first iteration will focus on just tracking number of available spots
# fixed parking lot size
# no license plates
# no timing / tickets
# all cars can park in all spots

from dataclasses import dataclass

@dataclass
class ParkingLot:

    capacity_per_level = 100

    LEVELS = [0, 0, 0]

    def park_car(self):
        for i in range(3):
            if self.LEVELS[i] < self.capacity_per_level:
                self.LEVELS[i] += 1
                return True
        
        return False
    
    def is_lot_full(self):
        return all([level == 100 for level in self.LEVELS])
            