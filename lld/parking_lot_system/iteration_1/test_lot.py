from .lot import ParkingLot

def test_park__lot_not_full():
    lot = ParkingLot()

    for _ in range(299):
        lot.park_car()
        assert lot.is_lot_full() == False

    lot.park_car()
    assert lot.is_lot_full() == True