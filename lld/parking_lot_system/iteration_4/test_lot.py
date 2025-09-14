from .lot import ParkingLot, ParkEvent, Car, ParkingLotLevel
import pytest

@pytest.fixture
def compact_car():
    return Car("12345", size=1)

@pytest.fixture
def regular_car():
    return Car("46234", size=5)

@pytest.fixture
def parking_lot():
    return ParkingLot(
        capacity_per_level=10,
        levels=10,
    )

@pytest.fixture
def parking_lot_level():
    return ParkingLotLevel(10, 2)


def _fill_lot_level(parks, level):
    for park in parks:
        car, time = park
        compact_spot = car.size <= 2
        level.cars_parked[car.license] = ParkEvent(car, time, compact_spot)
        if compact_spot:
            level.compact_spots_filled += 1
        else:
            level.regular_spots_filled += 1
        

def test_car__is_compact(compact_car, regular_car):
    assert compact_car.is_compact is True
    assert regular_car.is_compact is False


def test_lot__car_enters(mocker, parking_lot, compact_car):
    mock_enters_level = mocker.patch("lld.parking_lot_system.iteration_4.lot.ParkingLotLevel.car_enters")
    mock_enters_level.return_value = True
    result = parking_lot.car_enters(compact_car, 4, 2)
    assert result == True
    mock_enters_level.assert_called_once_with(compact_car, 4)
    assert isinstance(parking_lot.cars_parked.get("12345"), ParkingLotLevel)

def test_lot__car_enters_fails(mocker, parking_lot, compact_car):
    mock_enters_level = mocker.patch("lld.parking_lot_system.iteration_4.lot.ParkingLotLevel.car_enters")
    mock_enters_level.return_value = False
    result = parking_lot.car_enters(compact_car, 4, 2)
    assert result == False
    mock_enters_level.assert_called_once_with(compact_car, 4)
    assert parking_lot.cars_parked.get("12345") is None

def test_lot__car_leaves(mocker, parking_lot, compact_car):
    mock_enters_level = mocker.patch("lld.parking_lot_system.iteration_4.lot.ParkingLotLevel.car_leaves")
    mock_enters_level.return_value = True
    parking_lot.car_enters(compact_car, 4, 2)

    result = parking_lot.car_leaves(compact_car, 5)
    assert result == True
    mock_enters_level.assert_called_once_with(compact_car, 5)

def test_lot__car_leaves_fails(mocker, parking_lot, compact_car):
    mock_enters_level = mocker.patch("lld.parking_lot_system.iteration_4.lot.ParkingLotLevel.car_leaves")
    mock_enters_level.return_value = False
    parking_lot.car_enters(compact_car, 4, 2)
    
    result = parking_lot.car_leaves(compact_car, 5)
    assert result == False
    mock_enters_level.assert_called_once_with(compact_car, 5)

def test_lot__properties():
    parking_lot = ParkingLot(1, 1)
    assert parking_lot.total_capacity == 1
    assert parking_lot.capacity == 1
    assert parking_lot.is_lot_full == False

    parking_lot.car_enters(Car("1", 1), 15, 0)
    
    assert parking_lot.is_lot_full == True
    assert parking_lot.capacity == 0

def test_event(compact_car):
    event = ParkEvent(compact_car, 15, True)
    assert event.exit is None
    event.end(25)
    assert event.exit == 25

def test_level__properties(parking_lot_level):
    assert parking_lot_level.compact_capacity == 5
    assert parking_lot_level.regular_capacity
    assert parking_lot_level.open_spaces == 10
    assert parking_lot_level.open_regular_spaces == 5
    

def test_level__compact_cars_enter(mocker, parking_lot_level: ParkingLotLevel, compact_car: Car):
    mock_print = mocker.patch("lld.parking_lot_system.iteration_4.lot.print")

    parks = [
        (compact_car, 5),
        (Car("34533", 1), 15),
        (Car("3626", 1), 25),
        (Car("346346", 1), 25),
    ]

    _fill_lot_level(parks, parking_lot_level)

    assert set(parking_lot_level.cars_parked.keys()) == {"12345", "34533", "3626", "346346"}
    assert mock_print.call_count == 4

    for park in parks:
        car, enter_time = park

        event = parking_lot_level.cars_parked[car.license]
        assert isinstance(event, ParkEvent)    
        assert event.car.license == car.license
        assert event.compact_spot == True
        assert event.enter == enter_time
        assert event.exit is None

def test_level__compact_car_enters__compact_spots_filled(mocker, parking_lot_level, compact_car):
    mock_print = mocker.patch("lld.parking_lot_system.iteration_4.lot.print")
    parks = [
        (Car("90238", 1), 5),
        (Car("4345", 1), 5),
        (Car("6346", 1), 5),
        (Car("7657", 1), 5),
        (Car("734", 1), 5),
        (Car("3465", 5), 25),
    ]

    _fill_lot_level(parks, parking_lot_level)

    result = parking_lot_level.car_enters(compact_car, 26)
    assert result == True
    event = parking_lot_level.cars_parked[compact_car.license]
    assert event.compact_spot is False
    mock_print.assert_called_with("Car 12345 entered at 26.")


def test_level__compact_car_leaves(mocker, parking_lot_level, compact_car):
    mock_print = mocker.patch("lld.parking_lot_system.iteration_4.lot.print")
    parking_lot_level.car_enters(compact_car, 5)
    assert parking_lot_level.open_spaces == 9

    assert parking_lot_level.car_leaves(compact_car, 15) == True
    assert parking_lot_level.open_spaces == 10
    mock_print.assert_called_with("Car 12345 left at 15.")

def test_regular_car_enters(mocker, parking_lot_level: ParkingLotLevel, regular_car):
    mock_print = mocker.patch("lld.parking_lot_system.iteration_4.lot.print")

    parks = [
        (regular_car, 5),
        (Car("34533", 5), 15),
        (Car("3626", 5), 25),
        (Car("346346", 5), 25),
    ]

    _fill_lot_level(parks, parking_lot_level)

    assert set(parking_lot_level.cars_parked.keys()) == {"46234", "34533", "3626", "346346"}
    assert mock_print.call_count == 4

    for park in parks:
        car, enter_time = park
        
        event = parking_lot_level.cars_parked[car.license]
        assert isinstance(event, ParkEvent)    
        assert event.car.license == car.license
        assert event.compact_spot == False
        assert event.enter == enter_time
        assert event.exit is None

    parking_lot_level.open_spaces == 6
    parking_lot_level.open_regular_spaces == 1

def test_level__regular_car_leaves(mocker, parking_lot_level, regular_car):
    mock_print = mocker.patch("lld.parking_lot_system.iteration_4.lot.print")
    parking_lot_level.car_enters(regular_car, 5)
    assert parking_lot_level.open_spaces == 9

    assert parking_lot_level.car_leaves(regular_car, 15) == True
    assert parking_lot_level.open_spaces == 10
    mock_print.assert_called_with("Car 46234 left at 15.")
    
def test_level__full(mocker, compact_car):
    mocker.patch("lld.parking_lot_system.iteration_4.lot.print")
    level = ParkingLotLevel(1, 2)
    level.car_enters(compact_car, 23)
    assert level.is_full == True

def test_level__compact_car_enters__level_full(mocker, parking_lot_level, compact_car):
    mock_print = mocker.patch("lld.parking_lot_system.iteration_4.lot.print")
    parks = [
        (Car("90238", 1), 5),
        (Car("4345", 1), 5),
        (Car("6346", 1), 5),
        (Car("7657", 1), 5),
        (Car("734", 1), 5),
        (Car("34533", 5), 15),
        (Car("3626", 5), 25),
        (Car("346346", 5), 25),
        (Car("4536", 5), 25),
        (Car("3465", 5), 25),
    ]

    _fill_lot_level(parks, parking_lot_level)

    result = parking_lot_level.car_enters(compact_car, 30)
    assert result == False
    mock_print.assert_called_with("This level of the lot is full.")

def test_level__regular_car_enters__level_full(mocker, parking_lot_level, regular_car):
    mock_print = mocker.patch("lld.parking_lot_system.iteration_4.lot.print")
    parks = [
        (Car("90238", 1), 5),
        (Car("34533", 5), 15),
        (Car("3626", 5), 25),
        (Car("346346", 5), 25),
        (Car("4536", 5), 25),
        (Car("3465", 5), 25),
    ]

    _fill_lot_level(parks, parking_lot_level)

    result = parking_lot_level.car_enters(regular_car, 30)
    assert result == False
    mock_print.assert_called_with("This level of the lot is full for regular-sized cars.")

def test_level__car_enters__existing_car(mocker, parking_lot_level, compact_car):
    mock_print = mocker.patch("lld.parking_lot_system.iteration_4.lot.print")
    parking_lot_level.cars_parked[compact_car.license] = ParkEvent(compact_car, 5, True)

    result = parking_lot_level.car_enters(compact_car, 145)
    assert result == False
    mock_print.assert_called_with("This car 12345 is already parked!")

def test_level__car_leaves__nonexistent_car(mocker, parking_lot_level, compact_car):
    mock_print = mocker.patch("lld.parking_lot_system.iteration_4.lot.print")

    result = parking_lot_level.car_leaves(compact_car, 145)
    assert result == False
    mock_print.assert_called_with("This car 12345 has not parked here.")

def test_level__car_leaves__already_left(mocker, parking_lot_level, regular_car):
    mock_print = mocker.patch("lld.parking_lot_system.iteration_4.lot.print")
    parking_lot_level.cars_parked[regular_car.license] = ParkEvent(regular_car, 5, True, 10)

    result = parking_lot_level.car_leaves(regular_car, 145)
    assert result == False
    mock_print.assert_called_with("This car 46234 has already left the lot at 10.")

def test_level__car_leaves__exit_earlier_than_enter(mocker, parking_lot_level, regular_car):
    mock_print = mocker.patch("lld.parking_lot_system.iteration_4.lot.print")
    parking_lot_level.cars_parked[regular_car.license] = ParkEvent(regular_car, 5, True, 10)

    result = parking_lot_level.car_leaves(regular_car, 2)
    assert result == False
    mock_print.assert_called_with("This car 46234 cannot be leaving before it entered.")