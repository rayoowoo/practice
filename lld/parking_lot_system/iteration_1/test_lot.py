from .lot import ParkingLot

def test_park__lot_parks_cars():
    lot = ParkingLot()

    for _ in range(299):
        park_result = lot.park_car()
        assert park_result == True
        assert lot.is_lot_full() == False

    park_result = lot.park_car()
    assert park_result == True
    assert lot.is_lot_full() == True

    park_result = lot.park_car()
    assert park_result == False