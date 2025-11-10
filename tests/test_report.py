import datetime
import pytest
from unittest.mock import patch, MagicMock
from services.library_service import get_patron_status_report

def datetime_side_effect(*args, **kwargs):
    return datetime.datetime(*args, **kwargs)

def fromisoformat_side_effect(date_string):
    return datetime.datetime.fromisoformat(date_string)

MOCK_BORROWED_BOOKS = [
    {'book_id': 1, 'due_date': datetime.datetime(2000, 1, 15, 0, 0, 0)},
]

MOCK_BORROW_COUNT = 1

MOCK_BORROW_RECORDS = [
    {
        'book_id': 1,
        'title': 'Book One',
        'author': 'Author One',
        'borrow_date': '2000-01-01T00:00:00',
        'due_date': '2000-01-15T00:00:00',
        'return_date': None
    },
    {
        'book_id': 2,
        'title': 'Book Two',
        'author': 'Author Two',
        'borrow_date': '1999-12-01T00:00:00',
        'due_date': '1999-12-15T00:00:00',
        'return_date': '1999-12-10T00:00:00'
    }
]

class MockConnection:
    def execute(self, query, params):
        return self

    def fetchall(self):
        return MOCK_BORROW_RECORDS

    def close(self):
        pass

@patch("services.library_service.datetime")
@patch("services.library_service.get_patron_borrow_count")
@patch("services.library_service.get_db_connection")
@patch("services.library_service.get_patron_borrowed_books")
def test_fake(GET_BORROWED, GET_DB_CONN, GET_BORROW_COUNT, MOCK_DATETIME):
    report = get_patron_status_report("0")

    assert "must be exactly 6 digits" in report['status'].lower()

    GET_BORROWED.assert_not_called()
    GET_DB_CONN.assert_not_called()
    GET_BORROW_COUNT.assert_not_called()
    MOCK_DATETIME.now.assert_not_called()

@patch("services.library_service.datetime")
@patch("services.library_service.get_patron_borrow_count")
@patch("services.library_service.get_db_connection")
@patch("services.library_service.get_patron_borrowed_books")
def test_fetch_amt(GET_BORROWED, GET_DB_CONN, GET_BORROW_COUNT, MOCK_DATETIME):
    GET_BORROWED.return_value = MOCK_BORROWED_BOOKS
    GET_BORROW_COUNT.return_value = MOCK_BORROW_COUNT
    GET_DB_CONN.return_value = MockConnection()

    MOCK_DATETIME.now.return_value = datetime.datetime(2000, 1, 17, 0, 0, 0)
    MOCK_DATETIME.side_effect = datetime_side_effect
    MOCK_DATETIME.fromisoformat.side_effect = fromisoformat_side_effect

    report = get_patron_status_report("536892")

    assert "success" in report['status'].lower()
    assert isinstance(report['borrowed'], list)
    assert len(report['borrowed']) == len(MOCK_BORROWED_BOOKS)
    assert report['borrowedAmt'] == MOCK_BORROW_COUNT
    assert len(report['history']) == len(MOCK_BORROW_RECORDS)

    GET_BORROWED.assert_called_with("536892")
    GET_BORROW_COUNT.assert_called_once_with("536892")
    GET_DB_CONN.assert_called_once()

@patch("services.library_service.datetime")
@patch("services.library_service.get_patron_borrow_count")
@patch("services.library_service.get_db_connection")
@patch("services.library_service.get_patron_borrowed_books")
def test_fetch_borrowed(GET_BORROWED, GET_DB_CONN, GET_BORROW_COUNT, MOCK_DATETIME):
    GET_BORROWED.return_value = MOCK_BORROWED_BOOKS
    GET_BORROW_COUNT.return_value = MOCK_BORROW_COUNT
    GET_DB_CONN.return_value = MockConnection()

    MOCK_DATETIME.now.return_value = datetime.datetime(2000, 1, 17)
    MOCK_DATETIME.side_effect = datetime_side_effect
    MOCK_DATETIME.fromisoformat.side_effect = fromisoformat_side_effect

    report = get_patron_status_report("536892")

    assert report['borrowed'][0]['book_id'] == 1

    GET_BORROWED.assert_called_with("536892")
    GET_BORROW_COUNT.assert_called_once()
    GET_DB_CONN.assert_called_once()

@patch("services.library_service.datetime")
@patch("services.library_service.get_patron_borrow_count")
@patch("services.library_service.get_db_connection")
@patch("services.library_service.get_patron_borrowed_books")
def test_fetch_history1(GET_BORROWED, GET_DB_CONN, GET_BORROW_COUNT, MOCK_DATETIME):
    GET_BORROWED.return_value = MOCK_BORROWED_BOOKS
    GET_BORROW_COUNT.return_value = MOCK_BORROW_COUNT
    GET_DB_CONN.return_value = MockConnection()

    MOCK_DATETIME.now.return_value = datetime.datetime(2000, 1, 17)
    MOCK_DATETIME.side_effect = datetime_side_effect
    MOCK_DATETIME.fromisoformat.side_effect = fromisoformat_side_effect

    report = get_patron_status_report("536892")

    assert report['history'][0]['book_id'] == 1
    assert report['history'][0]['return_date'] is None

    GET_BORROWED.assert_called_with("536892")
    GET_BORROW_COUNT.assert_called_once()
    GET_DB_CONN.assert_called_once()

@patch("services.library_service.datetime")
@patch("services.library_service.get_patron_borrow_count")
@patch("services.library_service.get_db_connection")
@patch("services.library_service.get_patron_borrowed_books")
def test_fetch_history2(GET_BORROWED, GET_DB_CONN, GET_BORROW_COUNT, MOCK_DATETIME):
    GET_BORROWED.return_value = MOCK_BORROWED_BOOKS
    GET_BORROW_COUNT.return_value = MOCK_BORROW_COUNT
    GET_DB_CONN.return_value = MockConnection()

    MOCK_DATETIME.now.return_value = datetime.datetime(2000, 1, 17)
    MOCK_DATETIME.side_effect = datetime_side_effect
    MOCK_DATETIME.fromisoformat.side_effect = fromisoformat_side_effect

    report = get_patron_status_report("536892")

    assert report['history'][1]['book_id'] == 2
    assert report['history'][1]['return_date'] is not None

    GET_BORROWED.assert_called_with("536892")
    GET_BORROW_COUNT.assert_called_once()
    GET_DB_CONN.assert_called_once()