from .lot import ParkingLot, ParkEvent
import pytest

def test_car_enters():
    lot = ParkingLot()

    park_result = lot.car_enters("12345", 10)
    assert park_result == True

    park_event = lot.cars_parked.get("12345")
    assert isinstance(park_event, ParkEvent)
    assert park_event.license == "12345"
    assert park_event.level == 0
    assert park_event.enter == 10
    assert park_event.exit is None

def test_car_leaves():
    lot = ParkingLot()
    lot.car_enters("12345", 10)
    leave_result = lot.car_leaves("12345", 20)
    assert leave_result == True
    
    park_event = lot.cars_parked.get("12345")
    assert park_event.exit == 20
    
def test_lot_full(mocker):
    mock_print = mocker.patch("lld.parking_lot_system.iteration_2.lot.print")
    lot = ParkingLot()

    for i in range(299):
        park_result = lot.car_enters(str(i), i)
        assert park_result == True
        assert lot.is_lot_full() == False
        assert lot.capacity == 300 - i - 1

    park_result = lot.car_enters("299", 299)
    assert park_result == True
    assert lot.is_lot_full() == True

    park_result = lot.car_enters("300", 300)
    assert park_result == False
    mock_print.assert_called_with("The parking lot is full.")

def test_car_enters__existing_car(mocker):
    mock_print = mocker.patch("lld.parking_lot_system.iteration_2.lot.print")
    lot = ParkingLot()

    lot.car_enters("12345", 10)
    park_result = lot.car_enters("12345", 11)
    assert park_result == False
    mock_print.assert_called_with("This car 12345 is already parked!")

def test_car_leaves__nonexistent_car(mocker):
    mock_print = mocker.patch("lld.parking_lot_system.iteration_2.lot.print")
    lot = ParkingLot()

    lot.car_enters("12345", 10)
    leave_result = lot.car_leaves("3324", 30)
    assert leave_result == False
    mock_print.assert_called_with("This car 3324 has not parked here.")

def test_car_leaves__already_left(mocker):
    mock_print = mocker.patch("lld.parking_lot_system.iteration_2.lot.print")
    lot = ParkingLot()

    lot.car_enters("12345", 10)
    lot.car_leaves("12345", 20)
    leave_result = lot.car_leaves("12345", 30)
    assert leave_result == False
    mock_print.assert_called_with("This car 12345 has already left the lot at 20")

def test_car_leaves__exit_earlier_than_enter(mocker):
    mock_print = mocker.patch("lld.parking_lot_system.iteration_2.lot.print")
    lot = ParkingLot()

    lot.car_enters("12345", 10)
    leave_result = lot.car_leaves("12345", 9)
    assert leave_result == False
    mock_print.assert_called_with("This car 12345 cannot be leaving before it entered.")