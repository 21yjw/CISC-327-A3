import datetime
import pytest
from unittest.mock import patch
from services.library_service import (
    calculate_late_fee_for_book
)


@patch("services.library_service.datetime")
@patch("services.library_service.get_patron_borrowed_books")
def test_not_overdue(GET_BORROWED, DATETIME):
    BOOK_ID = 1
    DUE_DATE = datetime.datetime(2000, 1, 15)
    RETURN_DATE = datetime.datetime(2000, 1, 15)

    GET_BORROWED.return_value = [{"book_id": BOOK_ID, "due_date": DUE_DATE}]
    DATETIME.now.return_value = RETURN_DATE

    message = calculate_late_fee_for_book("123456", BOOK_ID)

    assert message == {'fee_amount': 0, 'days_overdue': 0, 'status': 'success'}

    GET_BORROWED.assert_called_once_with("123456")
    DATETIME.now.assert_called_once()


@patch("services.library_service.datetime")
@patch("services.library_service.get_patron_borrowed_books")
def test_overdue_first_7(GET_BORROWED, DATETIME):
    BOOK_ID = 2
    DUE_DATE = datetime.datetime(2000, 1, 15)
    RETURN_DATE = datetime.datetime(2000, 1, 17)

    GET_BORROWED.return_value = [{"book_id": BOOK_ID, "due_date": DUE_DATE}]
    DATETIME.now.return_value = RETURN_DATE

    message = calculate_late_fee_for_book("123456", BOOK_ID)

    assert message == {'fee_amount': 1.00, 'days_overdue': 2, 'status': 'success'}

    GET_BORROWED.assert_called_once_with("123456")
    DATETIME.now.assert_called_once()


@patch("services.library_service.datetime")
@patch("services.library_service.get_patron_borrowed_books")
def test_overdue_over_7(GET_BORROWED, DATETIME):
    BOOK_ID = 3
    DUE_DATE = datetime.datetime(2000, 1, 15)
    RETURN_DATE = datetime.datetime(2000, 1, 24)

    GET_BORROWED.return_value = [{"book_id": BOOK_ID, "due_date": DUE_DATE}]
    DATETIME.now.return_value = RETURN_DATE

    message = calculate_late_fee_for_book("123123", BOOK_ID)

    assert message == {'fee_amount': 5.50, 'days_overdue': 9, 'status': 'success'}

    GET_BORROWED.assert_called_once_with("123123")
    DATETIME.now.assert_called_once()


@patch("services.library_service.datetime")
@patch("services.library_service.get_patron_borrowed_books")
def test_overdue_fee_limit(GET_BORROWED, DATETIME):
    BOOK_ID = 1
    DUE_DATE = datetime.datetime(2000, 1, 15)
    RETURN_DATE = datetime.datetime(2000, 2, 20)

    GET_BORROWED.return_value = [{"book_id": BOOK_ID, "due_date": DUE_DATE}]
    DATETIME.now.return_value = RETURN_DATE

    message = calculate_late_fee_for_book("123456", BOOK_ID)

    assert message == {'fee_amount': 15, 'days_overdue': 36, 'status': 'success'}

    GET_BORROWED.assert_called_once_with("123456")
    DATETIME.now.assert_called_once()


@patch("services.library_service.datetime")
@patch("services.library_service.get_patron_borrowed_books")
def test_overdue_time_travel(GET_BORROWED, DATETIME):
    BOOK_ID = 1
    DUE_DATE = datetime.datetime(2001, 1, 15)
    RETURN_DATE = datetime.datetime(2000, 1, 1)

    GET_BORROWED.return_value = [{"book_id": BOOK_ID, "due_date": DUE_DATE}]
    DATETIME.now.return_value = RETURN_DATE

    message = calculate_late_fee_for_book("123456", BOOK_ID)

    assert message == {'fee_amount': 0, 'days_overdue': 0, 'status': 'success'}

    GET_BORROWED.assert_called_once_with("123456")
    DATETIME.now.assert_called_once()


@patch("services.library_service.datetime")
@patch("services.library_service.get_patron_borrowed_books")
def test_short_id(GET_BORROWED, DATETIME):
    message = calculate_late_fee_for_book("16", 1)
    assert 'must be exactly 6 digits' in message['status'].lower()

    GET_BORROWED.assert_not_called()
    DATETIME.now.assert_not_called()


@patch("services.library_service.datetime")
@patch("services.library_service.get_patron_borrowed_books")
def test_long_id(GET_BORROWED, DATETIME):
    message = calculate_late_fee_for_book("1234567", 1)
    assert 'must be exactly 6 digits' in message['status'].lower()

    GET_BORROWED.assert_not_called()
    DATETIME.now.assert_not_called()


@patch("services.library_service.datetime")
@patch("services.library_service.get_patron_borrowed_books")
def test_alphabetic_id(GET_BORROWED, DATETIME):
    message = calculate_late_fee_for_book("qwerty", 1)
    assert 'must be exactly 6 digits' in message['status'].lower()

    GET_BORROWED.assert_not_called()
    DATETIME.now.assert_not_called()


@patch("services.library_service.datetime")
@patch("services.library_service.get_patron_borrowed_books")
def test_fake_book(GET_BORROWED, DATETIME):
    GET_BORROWED.return_value = []
    DATETIME.now.return_value = datetime.datetime(2000, 1, 1)

    message = calculate_late_fee_for_book("123456", 900)

    assert 'could not find borrowed book' in message['status'].lower()

    GET_BORROWED.assert_called_once_with("123456")
    DATETIME.now.assert_not_called()