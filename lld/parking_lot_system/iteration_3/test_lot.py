from .lot import ParkingLot, ParkEvent
import pytest

def test_car_enters(mocker):
    mock_print = mocker.patch("lld.parking_lot_system.iteration_3.lot.print")
    lot = ParkingLot(capacity_per_level=25, levels=20)
    result = lot.car_enters("12345", 5, 2)
    assert result == True
    result = lot.car_enters("34533", 15, 18)
    assert result == True
    result = lot.car_enters("3626", 25, 15)
    assert result == True
    result = lot.car_enters("346346", 25, 15)
    assert result == True

    assert set(lot.cars_parked.keys()) == {"12345", "34533", "3626", "346346"}
    assert mock_print.call_count == 4
    
    assert isinstance(lot.cars_parked["12345"], ParkEvent)
    assert lot.cars_parked["12345"].license == "12345"
    assert lot.cars_parked["12345"].level == 2
    assert lot.cars_parked["12345"].enter == 5
    assert lot.cars_parked["12345"].exit is None
    
    assert isinstance(lot.cars_parked["34533"], ParkEvent)
    assert lot.cars_parked["34533"].license == "34533"
    assert lot.cars_parked["34533"].level == 18
    assert lot.cars_parked["34533"].enter == 15
    assert lot.cars_parked["34533"].exit is None
    
    assert isinstance(lot.cars_parked["3626"], ParkEvent)
    assert lot.cars_parked["3626"].license == "3626"
    assert lot.cars_parked["3626"].level == 15
    assert lot.cars_parked["3626"].enter == 25
    assert lot.cars_parked["3626"].exit is None
    
    assert isinstance(lot.cars_parked["346346"], ParkEvent)
    assert lot.cars_parked["346346"].license == "346346"
    assert lot.cars_parked["346346"].level == 15
    assert lot.cars_parked["346346"].enter == 25
    assert lot.cars_parked["346346"].exit is None

def test_car_leaves(mocker):
    mock_print = mocker.patch("lld.parking_lot_system.iteration_3.lot.print")
    lot = ParkingLot(capacity_per_level=1000, levels=200)

    lot.car_enters("12345", 5, 2)
    lot.car_enters("34533", 15, 18)
    lot.car_enters("3626", 25, 15)
    lot.car_enters("346346", 25, 15)

    leave_result = lot.car_leaves("12345", 50)
    assert leave_result == True
    assert lot.capacity == 200000 - 3

    
def test_lot_full(mocker):
    lot = ParkingLot(capacity_per_level=1, levels=1)
    
    lot.car_enters("12345", 5, 0)
    assert lot.is_lot_full() == True

def test_car_enters__invalid_level(mocker):
    mock_print = mocker.patch("lld.parking_lot_system.iteration_3.lot.print")
    lot = ParkingLot(capacity_per_level=1000, levels=200)

    park_result = lot.car_enters("12345", 11, 201)
    assert park_result == False
    mock_print.assert_called_with("There is no level above 200.")

def test_car_enters__level_full(mocker):
    mock_print = mocker.patch("lld.parking_lot_system.iteration_3.lot.print")
    lot = ParkingLot(capacity_per_level=1, levels=2)

    lot.car_enters("12345", 11, 1)
    park_result = lot.car_enters("345346", 12, 1)
    assert park_result == False
    mock_print.assert_called_with("Level 1 of the lot is full.")

def test_car_enters__existing_car(mocker):
    mock_print = mocker.patch("lld.parking_lot_system.iteration_3.lot.print")
    lot = ParkingLot(capacity_per_level=35, levels=3)

    lot.car_enters("12345", 10, 2)
    park_result = lot.car_enters("12345", 11, 1)
    assert park_result == False
    mock_print.assert_called_with("This car 12345 is already parked!")

def test_car_leaves__nonexistent_car(mocker):
    mock_print = mocker.patch("lld.parking_lot_system.iteration_3.lot.print")
    lot = ParkingLot(capacity_per_level=35, levels=4)

    lot.car_enters("12345", 10, 2)
    leave_result = lot.car_leaves("3324", 30)
    assert leave_result == False
    mock_print.assert_called_with("This car 3324 has not parked here.")

def test_car_leaves__already_left(mocker):
    mock_print = mocker.patch("lld.parking_lot_system.iteration_3.lot.print")
    lot = ParkingLot(capacity_per_level=456, levels=2)

    lot.car_enters("12345", 10, 0)
    lot.car_leaves("12345", 20)
    leave_result = lot.car_leaves("12345", 30)
    assert leave_result == False
    mock_print.assert_called_with("This car 12345 has already left the lot at 20")

def test_car_leaves__exit_earlier_than_enter(mocker):
    mock_print = mocker.patch("lld.parking_lot_system.iteration_3.lot.print")
    lot = ParkingLot(capacity_per_level=546, levels=23)

    lot.car_enters("12345", 10, 2)
    leave_result = lot.car_leaves("12345", 9)
    assert leave_result == False
    mock_print.assert_called_with("This car 12345 cannot be leaving before it entered.")