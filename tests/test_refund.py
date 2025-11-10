import pytest
from unittest.mock import patch
from services.library_service import refund_late_fee_payment

#test transaction id
@patch("services.payment_service.PaymentGateway")
def test_invalid_transaction_id(PAYMENT):
    TRAN_ID = "143623"
    AMT = 23.5
    
    PAYMENT_INSTANCE = PAYMENT.return_value
    
    success, msg = refund_late_fee_payment(TRAN_ID, AMT)
    
    assert success == False
    assert "invalid transaction id" in msg.lower()
    
    PAYMENT.assert_not_called();
    PAYMENT_INSTANCE.refund_payment.assert_not_called()
    PAYMENT_INSTANCE.refund_payment.assert_not_called()
    
    
#test refund amount
@patch("services.payment_service.PaymentGateway")
def test_refund_negative(PAYMENT):
    #test refund negative dollars
    TRAN_ID = "txn_143623"
    AMT = -1
    
    PAYMENT_INSTANCE = PAYMENT.return_value
    
    success, msg = refund_late_fee_payment(TRAN_ID, AMT)
    
    assert success == False
    assert "must be greater than 0" in msg.lower()
    
    PAYMENT.assert_not_called();
    PAYMENT_INSTANCE.refund_payment.assert_not_called()
    PAYMENT_INSTANCE.refund_payment.assert_not_called()
    
@patch("services.payment_service.PaymentGateway")
def test_refund_zero(PAYMENT):
    #test refund zero dollars
    TRAN_ID = "txn_143623"
    AMT = 0
    
    PAYMENT_INSTANCE = PAYMENT.return_value
    
    success, msg = refund_late_fee_payment(TRAN_ID, AMT)
    
    assert success == False
    assert "must be greater than 0" in msg.lower()
    
    PAYMENT.assert_not_called();
    PAYMENT_INSTANCE.refund_payment.assert_not_called()
    PAYMENT_INSTANCE.refund_payment.assert_not_called()

@patch("services.payment_service.PaymentGateway")
def test_refund_excess(PAYMENT):
    #test refund more than 15
    TRAN_ID = "txn_143623"
    AMT = 15.01
    
    PAYMENT_INSTANCE = PAYMENT.return_value
    
    success, msg = refund_late_fee_payment(TRAN_ID, AMT)
    
    assert success == False
    assert "exceeds maximum" in msg.lower()
    
    PAYMENT.assert_not_called();
    PAYMENT_INSTANCE.refund_payment.assert_not_called()
    PAYMENT_INSTANCE.refund_payment.assert_not_called()


#test successful payment
@patch("services.payment_service.PaymentGateway")
def test_payment_success(PAYMENT):
    TRAN_ID = "txn_143623"
    AMT = 15
    
    PAYMENT_INSTANCE = PAYMENT.return_value
    PAYMENT_INSTANCE.refund_payment.return_value = (
        True, #success
        "testing success msg" #msg
    )
    
    success, msg = refund_late_fee_payment(TRAN_ID, AMT, PAYMENT_INSTANCE)
    
    assert success == True
    assert "testing success msg" in msg.lower()
    
    PAYMENT_INSTANCE.refund_payment.assert_called_once()
    PAYMENT_INSTANCE.refund_payment.assert_called_with(TRAN_ID, AMT)
    

#test unsuccessful payment
@patch("services.payment_service.PaymentGateway")
def test_payment_fail(PAYMENT):
    TRAN_ID = "txn_143623"
    AMT = 15
    
    PAYMENT_INSTANCE = PAYMENT.return_value
    PAYMENT_INSTANCE.refund_payment.return_value = (
        False, #success
        "testing failure msg" #msg
    )
    
    success, msg = refund_late_fee_payment(TRAN_ID, AMT, PAYMENT_INSTANCE)
    
    assert success == False
    assert "refund failed" in msg.lower()
    
    PAYMENT_INSTANCE.refund_payment.assert_called_once()
    PAYMENT_INSTANCE.refund_payment.assert_called_with(TRAN_ID, AMT)
    
    
#test payment exception
#test unsuccessful payment
@patch("services.payment_service.PaymentGateway")
def test_payment_exception(PAYMENT):
    TRAN_ID = "txn_143623"
    AMT = 15
    
    PAYMENT_INSTANCE = PAYMENT.return_value
    PAYMENT_INSTANCE.refund_payment.side_effect = Exception("payment exception")
    
    success, msg = refund_late_fee_payment(TRAN_ID, AMT, PAYMENT_INSTANCE)
    
    assert success == False
    assert "refund processing error" in msg.lower()
    
    PAYMENT_INSTANCE.refund_payment.assert_called_once()
    PAYMENT_INSTANCE.refund_payment.assert_called_with(TRAN_ID, AMT)