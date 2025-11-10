import pytest
from unittest.mock import patch
from services.library_service import search_books_in_catalog

# Sample books data to use in mocks
MOCK_BOOKS = [
    {"isbn": "7240407438547", "title": "A Guide to Baking", "author": "Test Author"},
    {"isbn": "0642162625830", "title": "A Guide to Cooking", "author": "Test Author"},
    {"isbn": "7727833522326", "title": "A Guide to swimming", "author": "Test Author"},
    {"isbn": "1588427818151", "title": "swimming for beginners", "author": "Test Author"},
    {"isbn": "0862676087482", "title": "ahhhhhhhhhhh", "author": "Test Author"},
]

@patch("services.library_service.get_all_books")
def test_search_title_no_result(mock_get_all_books):
    mock_get_all_books.return_value = MOCK_BOOKS
    books = search_books_in_catalog("nothing", "title")
    assert len(books) == 0
    mock_get_all_books.assert_called_once()

@patch("services.library_service.get_all_books")
def test_search_author_no_result(mock_get_all_books):
    mock_get_all_books.return_value = MOCK_BOOKS
    books = search_books_in_catalog("no-one", "author")
    assert len(books) == 0
    mock_get_all_books.assert_called_once()

@patch("services.library_service.get_book_by_isbn")
def test_search_isbn_no_result(mock_get_book_by_isbn):
    mock_get_book_by_isbn.return_value = None
    books = search_books_in_catalog("2354356", "isbn")
    assert len(books) == 0
    mock_get_book_by_isbn.assert_called_once_with("2354356")

def test_search_invalid_type():
    books = search_books_in_catalog("paradox", "type type")
    assert len(books) == 0

@patch("services.library_service.get_all_books")
def test_search_title_one_result(mock_get_all_books):
    mock_get_all_books.return_value = MOCK_BOOKS
    books = search_books_in_catalog("baking", "title")
    assert len(books) == 1
    assert books[0]["title"].lower().find("baking") != -1
    mock_get_all_books.assert_called_once()

@patch("services.library_service.get_all_books")
def test_search_title_two_results(mock_get_all_books):
    mock_get_all_books.return_value = MOCK_BOOKS
    books = search_books_in_catalog("swimming", "title")
    assert len(books) == 2
    for book in books:
        assert "swimming" in book["title"].lower()
    mock_get_all_books.assert_called_once()

@patch("services.library_service.get_book_by_isbn")
def test_search_isbn_found(mock_get_book_by_isbn):
    mock_get_book_by_isbn.return_value = MOCK_BOOKS[-1]  # last book with isbn "0862676087482"
    books = search_books_in_catalog("0862676087482", "isbn")
    assert len(books) == 1
    assert books[0]["isbn"] == "0862676087482"
    mock_get_book_by_isbn.assert_called_once_with("0862676087482")