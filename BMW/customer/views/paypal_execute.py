import paypalrestsdk
import logging
logging.basicConfig(level=logging.INFO)

# ID of the payment. This ID is provided when creating payment.
payment = paypalrestsdk.Payment.find("PAY-28103131SP722473WKFD7VGQ")

# PayerID is required to approve the payment.
if payment.execute({"payer_id": "DUFRQ8GWYMJXC"}):  # return True or False
    print("Payment[%s] execute successfully" % (payment.id))
else:
    print(payment.error)