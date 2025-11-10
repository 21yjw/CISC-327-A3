import datetime
import pytest
from unittest.mock import patch
from services.library_service import return_book_by_patron

# Sample borrowed books mock data
MOCK_BORROWED_BOOKS = [
    {"book_id": 1, "title": "Test Book"},
    {"book_id": 2, "title": "Another Book"},
]

# Helper to patch datetime.datetime.now properly
def datetime_side_effect(*args, **kwargs):
    return datetime.datetime(*args, **kwargs)

@patch("services.library_service.datetime")
@patch("services.library_service.update_borrow_record_return_date")
@patch("services.library_service.update_book_availability")
@patch("services.library_service.get_patron_borrowed_books")
def test_default1(GET_BORROWED, UPDATE_AVAIL, UPDATE_RETURN, MOCK_DATETIME):
    patron_id = "123456"
    book_id = 1
    GET_BORROWED.return_value = [{"book_id": book_id, "title": "Test Book"}]

    MOCK_DATETIME.now.return_value = datetime.datetime(2023, 1, 1)
    MOCK_DATETIME.side_effect = datetime_side_effect

    success, message = return_book_by_patron(patron_id, book_id)
    
    assert success is True
    assert "successfully returned" in message.lower()

    GET_BORROWED.assert_called_once_with(patron_id)
    UPDATE_AVAIL.assert_called_once_with(book_id, 1)
    UPDATE_RETURN.assert_called_once_with(patron_id, book_id, MOCK_DATETIME.now.return_value)

@patch("services.library_service.datetime")
@patch("services.library_service.update_borrow_record_return_date")
@patch("services.library_service.update_book_availability")
@patch("services.library_service.get_patron_borrowed_books")
def test_default2(GET_BORROWED, UPDATE_AVAIL, UPDATE_RETURN, MOCK_DATETIME):
    patron_id = "123123"
    book_id = 2
    GET_BORROWED.return_value = [{"book_id": book_id, "title": "book of all time"}]

    MOCK_DATETIME.now.return_value = datetime.datetime(2023, 1, 2)
    MOCK_DATETIME.side_effect = datetime_side_effect

    success, message = return_book_by_patron(patron_id, book_id)
    
    assert success is True
    assert "successfully returned" in message.lower()

    GET_BORROWED.assert_called_once_with(patron_id)
    UPDATE_AVAIL.assert_called_once_with(book_id, 1)
    UPDATE_RETURN.assert_called_once_with(patron_id, book_id, MOCK_DATETIME.now.return_value)

@patch("services.library_service.datetime")
@patch("services.library_service.update_borrow_record_return_date")
@patch("services.library_service.update_book_availability")
@patch("services.library_service.get_patron_borrowed_books")
def test_default3(GET_BORROWED, UPDATE_AVAIL, UPDATE_RETURN, MOCK_DATETIME):
    patron_id = "456456"
    book_id = 3
    GET_BORROWED.return_value = [{"book_id": book_id, "title": "cookbook"}]

    MOCK_DATETIME.now.return_value = datetime.datetime(2023, 1, 3)
    MOCK_DATETIME.side_effect = datetime_side_effect

    success, message = return_book_by_patron(patron_id, book_id)
    
    assert success is True
    assert "successfully returned" in message.lower()

    GET_BORROWED.assert_called_once_with(patron_id)
    UPDATE_AVAIL.assert_called_once_with(book_id, 1)
    UPDATE_RETURN.assert_called_once_with(patron_id, book_id, MOCK_DATETIME.now.return_value)

@patch("services.library_service.datetime")
@patch("services.library_service.update_borrow_record_return_date")
@patch("services.library_service.update_book_availability")
@patch("services.library_service.get_patron_borrowed_books")
def test_default4(GET_BORROWED, UPDATE_AVAIL, UPDATE_RETURN, MOCK_DATETIME):
    patron_id = "987654"
    book_id = 4
    GET_BORROWED.return_value = [{"book_id": book_id, "title": "textbook"}]

    MOCK_DATETIME.now.return_value = datetime.datetime(2023, 1, 4)
    MOCK_DATETIME.side_effect = datetime_side_effect

    success, message = return_book_by_patron(patron_id, book_id)
    
    assert success is True
    assert "successfully returned" in message.lower()

    GET_BORROWED.assert_called_once_with(patron_id)
    UPDATE_AVAIL.assert_called_once_with(book_id, 1)
    UPDATE_RETURN.assert_called_once_with(patron_id, book_id, MOCK_DATETIME.now.return_value)

# Invalid patron ID tests

@patch("services.library_service.get_patron_borrowed_books")
def test_short_id(GET_BORROWED):
    # Invalid patron_id, so get_patron_borrowed_books should not be called.
    success, message = return_book_by_patron("1", 5)
    
    assert success is False
    assert "must be exactly 6 digits" in message.lower()
    GET_BORROWED.assert_not_called()

@patch("services.library_service.get_patron_borrowed_books")
def test_long_id(GET_BORROWED):
    success, message = return_book_by_patron("123456789", 6)
    
    assert success is False
    assert "must be exactly 6 digits" in message.lower()
    GET_BORROWED.assert_not_called()

@patch("services.library_service.get_patron_borrowed_books")
def test_alphabetic_id(GET_BORROWED):
    success, message = return_book_by_patron("qwerty", 7)
    
    assert success is False
    assert "must be exactly 6 digits" in message.lower()
    GET_BORROWED.assert_not_called()

# Fake patron and fake book tests

@patch("services.library_service.datetime")
@patch("services.library_service.update_borrow_record_return_date")
@patch("services.library_service.update_book_availability")
@patch("services.library_service.get_patron_borrowed_books")
def test_fake_patron(GET_BORROWED, UPDATE_AVAIL, UPDATE_RETURN, MOCK_DATETIME):
    patron_id = "000000"
    book_id = 8
    # No borrowed books for this patron
    GET_BORROWED.return_value = []
    UPDATE_AVAIL.return_value = True
    UPDATE_RETURN.return_value = None

    MOCK_DATETIME.now.return_value = datetime.datetime(2023, 1, 5)
    MOCK_DATETIME.side_effect = datetime_side_effect

    success, message = return_book_by_patron(patron_id, book_id)
    
    assert success is False
    assert "could not find borrowed book" in message.lower()

    GET_BORROWED.assert_called_once_with(patron_id)
    UPDATE_AVAIL.assert_called_once_with(book_id, 1)
    UPDATE_RETURN.assert_called_once_with(patron_id, book_id, MOCK_DATETIME.now.return_value)
    MOCK_DATETIME.now.assert_called_once()

@patch("services.library_service.datetime")
@patch("services.library_service.update_borrow_record_return_date")
@patch("services.library_service.update_book_availability")
@patch("services.library_service.get_patron_borrowed_books")
def test_fake_book(GET_BORROWED, UPDATE_AVAIL, UPDATE_RETURN, MOCK_DATETIME):
    patron_id = "123456"
    book_id = 900
    # Borrowed books without target book
    GET_BORROWED.return_value = [{"book_id": 1, "title": "Book1"}]
    UPDATE_AVAIL.return_value = True
    UPDATE_RETURN.return_value = None

    MOCK_DATETIME.now.return_value = datetime.datetime(2023, 1, 6)
    MOCK_DATETIME.side_effect = datetime_side_effect

    success, message = return_book_by_patron(patron_id, book_id)
    
    assert success is False
    assert "could not find borrowed book" in message.lower()

    GET_BORROWED.assert_called_once_with(patron_id)
    UPDATE_AVAIL.assert_called_once_with(book_id, 1)
    UPDATE_RETURN.assert_called_once_with(patron_id, book_id, MOCK_DATETIME.now.return_value)
    MOCK_DATETIME.now.assert_called_once()