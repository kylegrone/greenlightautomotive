'''
Created on Feb 16, 2016

@author: aroofi
'''
import paypalrestsdk

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import redirect 
import logging
logging.basicConfig(level=logging.INFO)

from django.core.urlresolvers import reverse


class paypal_payment():
    
    def __init__(self,dealer):
        self.config = paypalrestsdk.configure({
                             "mode": dealer.mode, # sandbox or live
                             "client_id": dealer.client_id,
                             "client_secret": dealer.secret })
    
    
    def save_creditcard(self , type , number , exp_month , exp_year ,cvv, f_name , l_name):
        self.config
        credit_card = paypalrestsdk.CreditCard({
            "type": type,
            "number": number,
            "expire_month": exp_month,
            "expire_year": exp_year,
            "cvv2": cvv,
            "first_name": f_name,
            "last_name": l_name,
            })
        if credit_card.create():
            print("CreditCard[%s] created successfully" % (credit_card.id))
        else:
            print("Error while creating CreditCard:")
            print(credit_card.error)

    def delete_creditcard(self, card_id):
        self.config
        credit_card = paypalrestsdk.CreditCard.find(card_id)
        if credit_card.delete():
            print("CreditCard deleted")
        else:
            print(credit_card.error)
            
    def find_creditcard(self , card_id):
        self.config
        try:
            
            credit_card = paypalrestsdk.CreditCard.find(card_id)
            print("Got CreditCard[%s]" % (credit_card.id))
        
        except paypalrestsdk.ResourceNotFound as error:
            print("CreditCard Not Found")
            
    def pay_with_creditcard(self):
        self.config
        payment = paypalrestsdk.Payment({
                    "intent": "sale",
                    "payer": {
                        "payment_method": "credit_card",
                        "funding_instruments": [{            
                                "credit_card": {
                                "type": "visa",
                                "number": "4417119669820331",
                                "expire_month": "11",
                                "expire_year": "2018",
                                "cvv2": "874",
                                "first_name": "Joe",
                                "last_name": "Shopper",
                
                                # address in a payment. [Optional]
                                "billing_address": {
                                    "line1": "52 N Main ST",
                                    "city": "Johnstown",
                                    "state": "OH",
                                    "postal_code": "43210",
                                    "country_code": "US"}}}]},
                    "transactions": [{
                
                        # ItemList
                        "item_list": {
                            "items": [{
                                "name": "item",
                                "sku": "item",
                                "price": "1.00",
                                "currency": "USD",
                                "quantity": 1}]},
                
                        "amount": {
                            "total": "1.00",
                            "currency": "USD"},
                        "description": "This is the payment transaction description."}]})
                
                # Create Payment and return status( True or False )
        if payment.create():
            print("Payment[%s] created successfully" % (payment.id))
        else:
            # Display Error message
            print("Error while creating payment:")
            print(payment.error)
    
    def paywith_creditcard_token(self,crdt_id,list_service,list_recommandation, total):
        self.config
        items = []
        for obj in list_service:
            itm = {}
            itm["name"] = obj.service.name
            itm["sku"] = obj.service.name
            itm["price"] = format(obj.price,'.2f')
            itm["currency"] = "USD"
            itm["quantity"] = 1
            items.append(itm)
        for obj in list_recommandation:
            itm = {}
            itm["name"] = obj.notes
            itm["sku"] = obj.notes
            itm["price"] = format(obj.price,'.2f')
            itm["currency"] = "USD"
            itm["quantity"] = 1
            items.append(itm)
            
        payment = paypalrestsdk.Payment({
                        "intent": "sale",
                        "payer": {
                            "payment_method": "credit_card",                
                                "funding_instruments": [{
                                "credit_card_token": {
                                    "credit_card_id": crdt_id}}]},
                        "transactions": [{
                    
                            # ItemList
                            "item_list": {
                                "items": items},
                            "amount": {
                                "total": format(total,'.2f'),
                                "currency": "USD"},
                            "description": "This is the payment transaction description."}]})

# Create Payment and return status
        result = {}
        if payment.create():
            result['id'] = payment.id 
            return result
        else:
            result['error'] = payment.error
            return result
            
    def paywith_paypal(self,list_service,list_recommandation,total,appt_id,domain):
        self.config
        items = []
        for obj in list_service:
            itm = {}
            itm["name"] = obj.service.name
            itm["sku"] = obj.service.name
            itm["price"] = format(obj.price,'.2f')
            itm["currency"] = "USD"
            itm["quantity"] = 1
            items.append(itm)
        for obj in list_recommandation:
            itm = {}
            itm["name"] = obj.notes
            itm["sku"] = obj.notes
            itm["price"] = format(obj.price,'.2f')
            itm["currency"] = "USD"
            itm["quantity"] = 1
            items.append(itm)
        payment = paypalrestsdk.Payment({
                        "intent": "sale",
                    
                        "payer": {
                            "payment_method": "paypal"},
                    
                        # Redirect URLs
                        "redirect_urls": {
                        
                            "return_url": "http://"+domain+reverse('customer:status_alert_index',kwargs={'appointment_id': appt_id}),
                            "cancel_url": "http://"+domain+reverse('customer:payment_status',kwargs={'appointment_id': appt_id})},
                    
                        "transactions": [{
                    
                            # ItemList
                            "item_list": {
                                "items": items},
                    
                            # Amount
                            # Let's you specify a payment amount.
                            "amount": {
                                "total": format(total ,'.2f'),
                                "currency": "USD"},
                            "description": "This is the payment transaction description."}]})
    
            # Create Payment and return status
        if payment.create():
            print("Payment[%s] created successfully" % (payment.id))
    # Redirect the user to given approval url
            redirect_url=""
            for link in payment.links:
                if link.method == "REDIRECT":
                    redirect_url = str(link.href)
                    print redirect_url
                    return {'redirect' :redirect_url }     
        else:
            print("Error while creating payment:")
            return {'error' : payment.error}
        
    def execute(self, payment_id , payer_id):
        self.config
        result = {}
        try:
            payment = paypalrestsdk.Payment.find(payment_id)
        except paypalrestsdk.ResourceNotFound as error:
            result['error'] = 'Payment ID Not Found'
            return result
        if payment.execute({"payer_id": payer_id}): 
            # return True or False
            print("Payment[%s] execute successfully" % (payment.id))
            result['id'] = payment.id
            return result
        else:
            print(payment.error)
            result['error'] = payment.error
            return result