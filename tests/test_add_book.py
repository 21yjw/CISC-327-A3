import pytest
from unittest.mock import patch
from services.library_service import (
    add_book_to_catalog
)


#tests that should pass(no edge cases)
@patch("services.library_service.insert_book")
@patch("services.library_service.get_book_by_isbn")
def test_default1(GET_BOOK, INSERT_BOOK):
    GET_BOOK.return_value = False
    
    #add five books
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    
    assert success == True
    assert "successfully added" in message.lower()
    
    GET_BOOK.assert_called_with("1234567890123")
    INSERT_BOOK.assert_called_with("Test Book", "Test Author", "1234567890123", 5, 5)
    
@patch("services.library_service.insert_book")
@patch("services.library_service.get_book_by_isbn")
def test_default2(GET_BOOK, INSERT_BOOK):
    GET_BOOK.return_value = False

    #add 3 books
    success, message = add_book_to_catalog("book of all time", "mr author", "2086271237464", 3)

    assert success == True
    assert "successfully added" in message.lower()

    GET_BOOK.assert_called_with("2086271237464")
    INSERT_BOOK.assert_called_with("book of all time", "mr author", "2086271237464", 3, 3)


@patch("services.library_service.insert_book")
@patch("services.library_service.get_book_by_isbn")
def test_default3(GET_BOOK, INSERT_BOOK):
    GET_BOOK.return_value = False

    #add one book
    success, message = add_book_to_catalog("cookbook", "smells nice", "7863662484406", 1)

    assert success == True
    assert "successfully added" in message.lower()

    GET_BOOK.assert_called_with("7863662484406")
    INSERT_BOOK.assert_called_with("cookbook", "smells nice", "7863662484406", 1, 1)


@patch("services.library_service.insert_book")
@patch("services.library_service.get_book_by_isbn")
def test_default4(GET_BOOK, INSERT_BOOK):
    GET_BOOK.return_value = False

    #add 200 books
    success, message = add_book_to_catalog("textbook", "money hungry university", "2566480740281", 200)

    assert success == True
    assert "successfully added" in message.lower()

    GET_BOOK.assert_called_with("2566480740281")
    INSERT_BOOK.assert_called_with("textbook", "money hungry university", "2566480740281", 200, 200)


#test titles
@patch("services.library_service.insert_book")
@patch("services.library_service.get_book_by_isbn")
def test_no_title(GET_BOOK, INSERT_BOOK):
    GET_BOOK.return_value = False

    #add a book with no title
    success, message = add_book_to_catalog("", "Test Author", "0241118655485", 5)

    assert success == False
    assert "title is required" in message.lower()

    GET_BOOK.assert_not_called()
    INSERT_BOOK.assert_not_called()


@patch("services.library_service.insert_book")
@patch("services.library_service.get_book_by_isbn")
def test_long_title(GET_BOOK, INSERT_BOOK):
    GET_BOOK.return_value = False

    #add a book with long title
    success, message = add_book_to_catalog("BOOK NAME" * 100, "Test Author", "8177807788531", 5)

    assert success == False
    assert "title must be less than 200 characters" in message.lower()

    GET_BOOK.assert_not_called()
    INSERT_BOOK.assert_not_called()


@patch("services.library_service.insert_book")
@patch("services.library_service.get_book_by_isbn")
def test_unicode_title(GET_BOOK, INSERT_BOOK):
    GET_BOOK.return_value = False

    #add a book with unicode title
    success, message = add_book_to_catalog("Ⲙⶦ⨳⇬⭠⤸␕⾽℁", "Test Author", "5511026386280", 5)

    assert success == True
    assert "successfully added" in message.lower()

    GET_BOOK.assert_called_with("5511026386280")
    INSERT_BOOK.assert_called_with("Ⲙⶦ⨳⇬⭠⤸␕⾽℁", "Test Author", "5511026386280", 5, 5)


#test author
@patch("services.library_service.insert_book")
@patch("services.library_service.get_book_by_isbn")
def test_no_author(GET_BOOK, INSERT_BOOK):
    GET_BOOK.return_value = False

    #add a book with no author
    success, message = add_book_to_catalog("what a book", "", "8325351602477", 5)

    assert success == False
    assert "author is required" in message.lower()

    GET_BOOK.assert_not_called()
    INSERT_BOOK.assert_not_called()


@patch("services.library_service.insert_book")
@patch("services.library_service.get_book_by_isbn")
def test_long_author(GET_BOOK, INSERT_BOOK):
    GET_BOOK.return_value = False

    #add a book with looong author name
    success, message = add_book_to_catalog("what a book", "This is a very looooooooong name" * 100, "3280410408884", 5)

    assert success == False
    assert "author must be less than 100 characters" in message.lower()

    GET_BOOK.assert_not_called()
    INSERT_BOOK.assert_not_called()


@patch("services.library_service.insert_book")
@patch("services.library_service.get_book_by_isbn")
def test_unicode_author(GET_BOOK, INSERT_BOOK):
    GET_BOOK.return_value = False

    #add a book with author name with unicode(for other languages)
    success, message = add_book_to_catalog("what a book", "◔⽂⦠⥆ⱇ⍅⩢⾠ℳ⇶⪨⭄⥰℁", "1234567890124", 5)

    assert success == True
    assert "successfully added" in message.lower()

    GET_BOOK.assert_called_with("1234567890124")
    INSERT_BOOK.assert_called_with("what a book", "◔⽂⦠⥆ⱇ⍅⩢⾠ℳ⇶⪨⭄⥰℁", "1234567890124", 5, 5)


#test isbn
@patch("services.library_service.insert_book")
@patch("services.library_service.get_book_by_isbn")
def test_no_ISBN(GET_BOOK, INSERT_BOOK):
    GET_BOOK.return_value = False

    #add a book with no ISBN
    success, message = add_book_to_catalog("what a book", "author here", "", 5)

    assert success == False
    assert "isbn is required" in message.lower() or "isbn must be exactly 13 digits" in message.lower()

    GET_BOOK.assert_not_called()
    INSERT_BOOK.assert_not_called()


@patch("services.library_service.insert_book")
@patch("services.library_service.get_book_by_isbn")
def test_alphabet_ISBN(GET_BOOK, INSERT_BOOK):
    GET_BOOK.return_value = False

    #add a book with a alphabetic ISBN
    success, message = add_book_to_catalog("what a book", "author here", "QWERTYUIOPASD", 5)

    assert success == False
    assert "isbn must be exactly 13 digits" in message.lower()

    GET_BOOK.assert_not_called()
    INSERT_BOOK.assert_not_called()


@patch("services.library_service.insert_book")
@patch("services.library_service.get_book_by_isbn")
def test_mixed_ISBN(GET_BOOK, INSERT_BOOK):
    GET_BOOK.return_value = False

    #add a book with a ISBN with random garbage
    success, message = add_book_to_catalog("what a book", "author here", "\r*?\u0346&fish\u0000noh", 5)

    assert success == False
    assert "isbn must be exactly 13 digits" in message.lower()

    GET_BOOK.assert_not_called()
    INSERT_BOOK.assert_not_called()


@patch("services.library_service.insert_book")
@patch("services.library_service.get_book_by_isbn")
def test_short_ISBN(GET_BOOK, INSERT_BOOK):
    GET_BOOK.return_value = False

    #add a book with a short ISBN
    success, message = add_book_to_catalog("what a book", "author here", "123", 5)

    assert success == False
    assert "isbn must be exactly 13 digits" in message.lower()

    GET_BOOK.assert_not_called()
    INSERT_BOOK.assert_not_called()


@patch("services.library_service.insert_book")
@patch("services.library_service.get_book_by_isbn")
def test_long_ISBN(GET_BOOK, INSERT_BOOK):
    GET_BOOK.return_value = False

    #add a book with a long ISBN
    success, message = add_book_to_catalog("what a book", "author here", "123" * 10, 5)

    assert success == False
    assert "isbn must be exactly 13 digits" in message.lower()

    GET_BOOK.assert_not_called()
    INSERT_BOOK.assert_not_called()


#test copies
@patch("services.library_service.insert_book")
@patch("services.library_service.get_book_by_isbn")
def test_negative_books(GET_BOOK, INSERT_BOOK):
    GET_BOOK.return_value = False

    #add negative books
    success, message = add_book_to_catalog("what a book", "author here", "8531408773118", -1)

    assert success == False
    assert "total copies must be a positive integer" in message.lower()

    GET_BOOK.assert_not_called()
    INSERT_BOOK.assert_not_called()


@patch("services.library_service.insert_book")
@patch("services.library_service.get_book_by_isbn")
def test_zero_books(GET_BOOK, INSERT_BOOK):
    GET_BOOK.return_value = False

    #add zero books
    success, message = add_book_to_catalog("what a book", "author here", "8165243131526", 0)

    assert success == False
    assert "total copies must be a positive integer" in message.lower()

    GET_BOOK.assert_not_called()
    INSERT_BOOK.assert_not_called()
    
@patch("services.library_service.insert_book")
@patch("services.library_service.get_book_by_isbn")
def test_duplicate_books(GET_BOOK, INSERT_BOOK):
    GET_BOOK.return_value = True

    #add zero books
    success, message = add_book_to_catalog("what a book", "author here", "8165243131526", 5)

    assert success == False
    assert "already exists" in message.lower()

    GET_BOOK.assert_called_with("8165243131526")
    INSERT_BOOK.assert_not_called()
    
@patch("services.library_service.insert_book")
@patch("services.library_service.get_book_by_isbn")
def test_database_err(GET_BOOK, INSERT_BOOK):
    GET_BOOK.return_value = False
    INSERT_BOOK.return_value = False

    #add zero books
    success, message = add_book_to_catalog("what a book", "author here", "8175243131526", 5)

    assert success == False
    assert "database error" in message.lower()

    GET_BOOK.assert_called_with("8175243131526")
    INSERT_BOOK.assert_called_with("what a book", "author here", "8175243131526", 5, 5)
