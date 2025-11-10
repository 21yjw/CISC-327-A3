import pytest
from unittest.mock import patch
from services.library_service import borrow_book_by_patron



# tests that should pass (no edge cases)
@patch("services.library_service.insert_borrow_record")
@patch("services.library_service.update_book_availability")
@patch("services.library_service.get_patron_borrow_count")
@patch("services.library_service.get_book_by_id")
def test_default1(GET_BOOK, BORROW_COUNT, UPDATE_AVAIL, INSERT_BORROW):
    GET_BOOK.return_value = {"title": "test book", "available_copies": 1}
    BORROW_COUNT.return_value = 0

    success, message = borrow_book_by_patron("123456", 1)

    assert success is True
    assert "successfully borrowed" in message.lower()

    GET_BOOK.assert_called_with(1)
    BORROW_COUNT.assert_called_with("123456")
    UPDATE_AVAIL.assert_called_once_with(1, -1)
    INSERT_BORROW.assert_called_once()


@patch("services.library_service.insert_borrow_record")
@patch("services.library_service.update_book_availability")
@patch("services.library_service.get_patron_borrow_count")
@patch("services.library_service.get_book_by_id")
def test_default2(GET_BOOK, BORROW_COUNT, UPDATE_AVAIL, INSERT_BORROW):
    GET_BOOK.return_value = {"title": "test book", "available_copies": 3}
    BORROW_COUNT.return_value = 0

    success, message = borrow_book_by_patron("123123", 2)

    assert success is True
    assert "successfully borrowed" in message.lower()

    GET_BOOK.assert_called_with(2)
    BORROW_COUNT.assert_called_with("123123")
    UPDATE_AVAIL.assert_called_once_with(2, -1)
    INSERT_BORROW.assert_called_once()


@patch("services.library_service.insert_borrow_record")
@patch("services.library_service.update_book_availability")
@patch("services.library_service.get_patron_borrow_count")
@patch("services.library_service.get_book_by_id")
def test_default3(GET_BOOK, BORROW_COUNT, UPDATE_AVAIL, INSERT_BORROW):
    GET_BOOK.return_value = {"title": "test book", "available_copies": 1}
    BORROW_COUNT.return_value = 0

    success, message = borrow_book_by_patron("456456", 3)

    assert success is True
    assert "successfully borrowed" in message.lower()

    GET_BOOK.assert_called_with(3)
    BORROW_COUNT.assert_called_with("456456")
    UPDATE_AVAIL.assert_called_once_with(3, -1)
    INSERT_BORROW.assert_called_once()


@patch("services.library_service.insert_borrow_record")
@patch("services.library_service.update_book_availability")
@patch("services.library_service.get_patron_borrow_count")
@patch("services.library_service.get_book_by_id")
def test_default4(GET_BOOK, BORROW_COUNT, UPDATE_AVAIL, INSERT_BORROW):
    GET_BOOK.return_value = {"title": "test book", "available_copies": 200}
    BORROW_COUNT.return_value = 0

    success, message = borrow_book_by_patron("987654", 4)

    assert success is True
    assert "successfully borrowed" in message.lower()

    GET_BOOK.assert_called_with(4)
    BORROW_COUNT.assert_called_with("987654")
    UPDATE_AVAIL.assert_called_once_with(4, -1)
    INSERT_BORROW.assert_called_once()


# test patron id validations (no DB calls)
@patch("services.library_service.insert_borrow_record")
@patch("services.library_service.update_book_availability")
@patch("services.library_service.get_patron_borrow_count")
@patch("services.library_service.get_book_by_id")
def test_short_id(GET_BOOK, BORROW_COUNT, UPDATE_AVAIL, INSERT_BORROW):
    success, message = borrow_book_by_patron("1", 5)

    assert success is False
    assert "must be exactly 6 digits" in message.lower()

    GET_BOOK.assert_not_called()
    BORROW_COUNT.assert_not_called()
    UPDATE_AVAIL.assert_not_called()
    INSERT_BORROW.assert_not_called()


@patch("services.library_service.insert_borrow_record")
@patch("services.library_service.update_book_availability")
@patch("services.library_service.get_patron_borrow_count")
@patch("services.library_service.get_book_by_id")
def test_long_id(GET_BOOK, BORROW_COUNT, UPDATE_AVAIL, INSERT_BORROW):
    success, message = borrow_book_by_patron("123456789", 6)

    assert success is False
    assert "must be exactly 6 digits" in message.lower()

    GET_BOOK.assert_not_called()
    BORROW_COUNT.assert_not_called()
    UPDATE_AVAIL.assert_not_called()
    INSERT_BORROW.assert_not_called()


@patch("services.library_service.insert_borrow_record")
@patch("services.library_service.update_book_availability")
@patch("services.library_service.get_patron_borrow_count")
@patch("services.library_service.get_book_by_id")
def test_alphabetic_id(GET_BOOK, BORROW_COUNT, UPDATE_AVAIL, INSERT_BORROW):
    success, message = borrow_book_by_patron("qwerty", 7)

    assert success is False
    assert "must be exactly 6 digits" in message.lower()

    GET_BOOK.assert_not_called()
    BORROW_COUNT.assert_not_called()
    UPDATE_AVAIL.assert_not_called()
    INSERT_BORROW.assert_not_called()


# test book existence
@patch("services.library_service.insert_borrow_record")
@patch("services.library_service.update_book_availability")
@patch("services.library_service.get_patron_borrow_count")
@patch("services.library_service.get_book_by_id")
def test_book_exists(GET_BOOK, BORROW_COUNT, UPDATE_AVAIL, INSERT_BORROW):
    PATRON_ID = "834246"
    BOOK_ID = 4354364

    GET_BOOK.return_value = None
    BORROW_COUNT.return_value = 0

    success, message = borrow_book_by_patron(PATRON_ID, BOOK_ID)

    assert success is False
    assert "book not found" in message.lower()

    GET_BOOK.assert_called_with(BOOK_ID)
    BORROW_COUNT.assert_not_called()
    UPDATE_AVAIL.assert_not_called()
    INSERT_BORROW.assert_not_called()

#database errors
@patch("services.library_service.insert_borrow_record")
@patch("services.library_service.update_book_availability")
@patch("services.library_service.get_patron_borrow_count")
@patch("services.library_service.get_book_by_id")
def test_insert_record_err(GET_BOOK, BORROW_COUNT, UPDATE_AVAIL, INSERT_BORROW):
    PATRON_ID = "834246"
    BOOK_ID = 43

    GET_BOOK.return_value = {"title": "test book", "available_copies": 3}
    BORROW_COUNT.return_value = 0
    INSERT_BORROW.return_value = False
    

    success, message = borrow_book_by_patron(PATRON_ID, BOOK_ID)

    assert success is False
    assert "database error" in message.lower()

    GET_BOOK.assert_called_with(BOOK_ID)
    BORROW_COUNT.assert_called_once()
    INSERT_BORROW.assert_called_once()
    UPDATE_AVAIL.assert_not_called()

@patch("services.library_service.insert_borrow_record")
@patch("services.library_service.update_book_availability")
@patch("services.library_service.get_patron_borrow_count")
@patch("services.library_service.get_book_by_id")
def test_update_avail_err(GET_BOOK, BORROW_COUNT, UPDATE_AVAIL, INSERT_BORROW):
    PATRON_ID = "834246"
    BOOK_ID = 43

    GET_BOOK.return_value = {"title": "test book", "available_copies": 3}
    BORROW_COUNT.return_value = 0
    INSERT_BORROW.return_value = True
    UPDATE_AVAIL.return_value = False
    

    success, message = borrow_book_by_patron(PATRON_ID, BOOK_ID)

    assert success is False
    assert "database error" in message.lower()

    GET_BOOK.assert_called_with(BOOK_ID)
    BORROW_COUNT.assert_called_once()
    INSERT_BORROW.assert_called_once()
    UPDATE_AVAIL.assert_called_once();


# test book availability and borrow limit
@patch("services.library_service.insert_borrow_record")
@patch("services.library_service.update_book_availability")
@patch("services.library_service.get_patron_borrow_count")
@patch("services.library_service.get_book_by_id")
def test_book_avaliable(GET_BOOK, BORROW_COUNT, UPDATE_AVAIL, INSERT_BORROW):
    PATRON_ID = "111111"
    BOOK_ID = 8

    # first borrow
    GET_BOOK.return_value = {"title": "test book", "available_copies": 1}
    BORROW_COUNT.return_value = 0

    success, message = borrow_book_by_patron(PATRON_ID, BOOK_ID)
    assert success is True
    assert "successfully borrowed" in message.lower()

    # second borrow with no copies available
    GET_BOOK.return_value = {"title": "test book", "available_copies": 0}
    BORROW_COUNT.return_value = 1

    success, message = borrow_book_by_patron(PATRON_ID, BOOK_ID)

    assert success is False
    assert "book is currently not available" in message.lower()

    GET_BOOK.assert_called_with(BOOK_ID)
    BORROW_COUNT.assert_called_with(PATRON_ID)
    UPDATE_AVAIL.assert_called_once_with(BOOK_ID, -1)
    INSERT_BORROW.assert_called_once() 


# test borrow limit enforcement
@patch("services.library_service.insert_borrow_record")
@patch("services.library_service.update_book_availability")
@patch("services.library_service.get_patron_borrow_count")
@patch("services.library_service.get_book_by_id")
def test_book_overborrow(GET_BOOK, BORROW_COUNT, UPDATE_AVAIL, INSERT_BORROW):
    PATRON_ID = "222222"
    BOOK_ID = 9
    MAX_BORROW_LIMIT = 5

    borrowed = -1

    def get_borrow_count(patron_id):
        nonlocal borrowed
        borrowed += 1
        return borrowed

    BORROW_COUNT.side_effect = get_borrow_count
    GET_BOOK.return_value = {"title": "test book", "available_copies": 100}

    for i in range(10):
        success, message = borrow_book_by_patron(PATRON_ID, BOOK_ID)

        if i < MAX_BORROW_LIMIT:
            assert success is True
            assert "successfully borrowed" in message.lower()
            
        else:
            assert success is False
            assert "reached the maximum borrowing limit" in message.lower()

        GET_BOOK.assert_called_with(BOOK_ID)
        BORROW_COUNT.assert_called_with(PATRON_ID)