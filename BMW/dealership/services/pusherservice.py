'''
Created on 27-Nov-2015

@author: Asim Riaz
'''
from cent.core import Client

class PusherService():
    client = None
    
    
    def connect(self,url,secret):
        """
            This method is used to connect to centrifuge server
        """
        self.client = Client(url,secret)
        
        

    def update_clients(self,channel,services,data):
        """
                This method is used to send message to centrifuge server
                
        """
        data = {"data": {"services":services,"data":data
                                
                                },"channel":channel}
        self.client.add("publish",data)
        try:
            result = self.send_message(data)
            if result:
                print result
                return result
            return None
        except Exception,e:
            print e
            pass

    def send_message(self,data):
        """
                This method is used to send message to centrifuge server
                
        """
       
        try:
            result,error = self.client.send()
            print error
            if result:
                return result
            return error
        except:
            pass
        



