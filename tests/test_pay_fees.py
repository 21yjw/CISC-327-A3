import pytest
from unittest.mock import patch
from services.library_service import pay_late_fees


#test patron_id invalid
@patch("services.payment_service.PaymentGateway")
@patch("services.library_service.get_book_by_id")
@patch("services.library_service.calculate_late_fee_for_book")
def test_patron_id_short(CALC_FEE, GET_BOOK, PAYMENT):
    #test short id
    success, msg, txn = pay_late_fees("12345", 12345)
    
    assert success == False;
    assert "invalid patron id" in msg.lower()
    assert txn == None
    
    CALC_FEE.assert_not_called()
    GET_BOOK.assert_not_called()
    PAYMENT.assert_not_called()

@patch("services.payment_service.PaymentGateway")
@patch("services.library_service.get_book_by_id")
@patch("services.library_service.calculate_late_fee_for_book")
def test_patron_id_long(CALC_FEE, GET_BOOK, PAYMENT):
    #test long id
    success, msg, txn = pay_late_fees("1234567", 12345)
    
    assert success == False;
    assert "invalid patron id" in msg.lower()
    assert txn == None
    
    CALC_FEE.assert_not_called()
    GET_BOOK.assert_not_called()
    PAYMENT.assert_not_called()

@patch("services.payment_service.PaymentGateway")
@patch("services.library_service.get_book_by_id")
@patch("services.library_service.calculate_late_fee_for_book")
def test_patron_id_alphabetic(CALC_FEE, GET_BOOK, PAYMENT):
    #test long id
    success, msg, txn = pay_late_fees("abcdef", 12345)
    
    assert success == False;
    assert "invalid patron id" in msg.lower()
    assert txn == None
    
    CALC_FEE.assert_not_called()
    GET_BOOK.assert_not_called()
    PAYMENT.assert_not_called()


#test fees invalid
@patch("services.payment_service.PaymentGateway")
@patch("services.library_service.get_book_by_id")
@patch("services.library_service.calculate_late_fee_for_book")
def test_no_fees(CALC_FEE, GET_BOOK, PAYMENT):
    #test no fees owed
    CALC_FEE.return_value = {
        "fee_amount": 0
    }
    
    success, msg, txn = pay_late_fees("123456", 12345)
    
    assert success == False;
    assert "no late fees" in msg.lower()
    assert txn == None
    
    CALC_FEE.assert_called_once()
    GET_BOOK.assert_not_called()
    PAYMENT.assert_not_called();
    
@patch("services.payment_service.PaymentGateway")
@patch("services.library_service.get_book_by_id")
@patch("services.library_service.calculate_late_fee_for_book")
def test_negative_fees(CALC_FEE, GET_BOOK, PAYMENT):
    #test negative fees owed
    CALC_FEE.return_value = {
        "fee_amount": -1
    }
    
    success, msg, txn = pay_late_fees("123456", 12345)
    
    assert success == False;
    assert "no late fees" in msg.lower()
    assert txn == None
    
    CALC_FEE.assert_called_once()
    GET_BOOK.assert_not_called()
    PAYMENT.assert_not_called();

@patch("services.payment_service.PaymentGateway")
@patch("services.library_service.get_book_by_id")
@patch("services.library_service.calculate_late_fee_for_book")
def test_missing_fees(CALC_FEE, GET_BOOK, PAYMENT):
    #test negative fees owed
    CALC_FEE.return_value = {}
    
    success, msg, txn = pay_late_fees("123456", 12345)
    
    assert success == False;
    assert "unable to calculate" in msg.lower()
    assert txn == None
    
    CALC_FEE.assert_called_once()
    GET_BOOK.assert_not_called()
    PAYMENT.assert_not_called();

#test invalid book
@patch("services.payment_service.PaymentGateway")
@patch("services.library_service.get_book_by_id")
@patch("services.library_service.calculate_late_fee_for_book")
def test_invalid_book(CALC_FEE, GET_BOOK, PAYMENT):
    #test negative fees owed
    CALC_FEE.return_value = {
        "fee_amount": 10
    }
    GET_BOOK.return_value = None
    
    success, msg, txn = pay_late_fees("123456", 12345)
    
    assert success == False;
    assert "book not found" in msg.lower()
    assert txn == None
    
    CALC_FEE.assert_called_once()
    GET_BOOK.assert_called_once()
    GET_BOOK.assert_called_with(12345)
    PAYMENT.assert_not_called();

#test invalid payment
@patch("services.payment_service.PaymentGateway")
@patch("services.library_service.get_book_by_id")
@patch("services.library_service.calculate_late_fee_for_book")
def test_pay_fee_invalid(CALC_FEE, GET_BOOK, PAYMENT):
    PATRON_ID = "123456"
    BOOK_ID = 12345
    AMT = 10
    TITLE = "book title"
    
    CALC_FEE.return_value = {
        "fee_amount": AMT
    }
    GET_BOOK.return_value = {
        "title": TITLE
    }
    PAYMENT_INSTANCE = PAYMENT.return_value
    PAYMENT_INSTANCE.process_payment.return_value = (
        False, #success
        1, #transaction_id
        "testing error message" #message
    )
    
    success, msg, txn = pay_late_fees(PATRON_ID, BOOK_ID, PAYMENT_INSTANCE)
    
    assert success == False
    assert "payment failed" in msg.lower();
    assert txn == None
    
    CALC_FEE.assert_called_once()
    CALC_FEE.assert_called_with(PATRON_ID, BOOK_ID)
    GET_BOOK.assert_called_once()
    GET_BOOK.assert_called_with(BOOK_ID)
    PAYMENT_INSTANCE.process_payment.assert_called_once()
    PAYMENT_INSTANCE.process_payment.assert_called_with(patron_id=PATRON_ID, amount=AMT, description=f"Late fees for '{TITLE}'")
    
#test valid payment
@patch("services.payment_service.PaymentGateway")
@patch("services.library_service.get_book_by_id")
@patch("services.library_service.calculate_late_fee_for_book")
def test_pay_fee_success(CALC_FEE, GET_BOOK, PAYMENT):
    PATRON_ID = "123456"
    BOOK_ID = 12345
    TRAN_ID = 485
    AMT = 10
    TITLE = "book title"
    
    CALC_FEE.return_value = {
        "fee_amount": AMT
    }
    GET_BOOK.return_value = {
        "title": TITLE
    }
    PAYMENT_INSTANCE = PAYMENT.return_value
    PAYMENT_INSTANCE.process_payment.return_value = (
        True, #success
        TRAN_ID, #transaction_id
        "testing success message" #message
    )
    
    success, msg, txn = pay_late_fees(PATRON_ID, BOOK_ID, PAYMENT_INSTANCE)
    
    assert success == True
    assert "payment success" in msg.lower();
    assert txn == TRAN_ID
    
    CALC_FEE.assert_called_once()
    CALC_FEE.assert_called_with(PATRON_ID, BOOK_ID)
    GET_BOOK.assert_called_once()
    GET_BOOK.assert_called_with(BOOK_ID)
    PAYMENT_INSTANCE.process_payment.assert_called_once()
    PAYMENT_INSTANCE.process_payment.assert_called_with(patron_id=PATRON_ID, amount=AMT, description=f"Late fees for '{TITLE}'")
    
#test netword error
@patch("services.payment_service.PaymentGateway")
@patch("services.library_service.get_book_by_id")
@patch("services.library_service.calculate_late_fee_for_book")
def test_pay_fee_exception(CALC_FEE, GET_BOOK, PAYMENT):
    PATRON_ID = "123456"
    BOOK_ID = 12345
    AMT = 10
    TITLE = "book title"
    
    CALC_FEE.return_value = {
        "fee_amount": AMT
    }
    GET_BOOK.return_value = {
        "title": TITLE
    }
    PAYMENT_INSTANCE = PAYMENT.return_value
    PAYMENT_INSTANCE.process_payment.side_effect = Exception("testing network error")
    
    success, msg, txn = pay_late_fees(PATRON_ID, BOOK_ID, PAYMENT_INSTANCE)
    
    assert success == False
    assert "payment processing error" in msg.lower();
    assert txn == None
    
    CALC_FEE.assert_called_once()
    CALC_FEE.assert_called_with(PATRON_ID, BOOK_ID)
    GET_BOOK.assert_called_once()
    GET_BOOK.assert_called_with(BOOK_ID)
    PAYMENT_INSTANCE.process_payment.assert_called_once()
    PAYMENT_INSTANCE.process_payment.assert_called_with(patron_id=PATRON_ID, amount=AMT, description=f"Late fees for '{TITLE}'")