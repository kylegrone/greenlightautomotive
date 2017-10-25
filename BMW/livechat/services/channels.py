'''
Created on 22-Nov-2015

@author: asimriaz
'''
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import models
from livechat.models import Channels


class ChannelService(object):
    """
            This class is used as a service layer for channels( CHat sesions).
            It is used to get all the information about the chat sessions
    
    """

    def add_chat_count(self,user_id):
        """
                THis method is used to add chat count for a user. if a user has  a chat session open
                this method should be used to update the count
        """
        try:
            user= User.objects.get(id=user_id)
            user.userprofile.number_of_chats =  user.userprofile.number_of_chats +1
            user.userprofile.save() 
            return True
        except:
            return False
    
    def delete_chat_count(self,user_id):
        """
                THis method is used to delete chat count for a user. if a user has  a chat session disconnected
                this method should be used to update the count
        """
        try:
            user= User.objects.get(id=user_id)
            user.userprofile.number_of_chats =  user.userprofile.number_of_chats -1
            if  user.userprofile.number_of_chats  <0:
                user.userprofile.number_of_chats = 0
            user.userprofile.save() 
            return True
        except:
            return False
        
    def saveChanneldForAdvisor(self,channel,guest_user,advisor):
        """
                This method is used to save the channe; for an advisor . Channels are basically the chat sessions
                
        """
        if self.getchannel(channel,guest_user,advisor) ==None:
                try:
                    channel =  Channels(channel=channel,guest_user=guest_user,advisor_id=advisor)
                    channel.save()
                    return True
                except:
                    return False
        return False
        
    def deleteChannel(self,channel,guest_user,advisor):
        """
            This method is used to delete chat sessions for an advisor.
        """
        channel = self.getchannel(channel,guest_user,advisor)
        if channel !=None:
                try:
#                     channel =  Channels(channel=channel,guest_user=guest_user,advisor_id=advisor)
                    channel.delete()
                    return True
                except:
                    return False
                return False
        
    def getchannel(self,channel_name,guest_user,advisor):
        """    
                This method is used to get a channel (chat session) for an advisor based on
                 the paraeters defined
        """
        channel = None
        try:
            channel = Channels.objects.filter(channel=channel_name,guest_user=guest_user,advisor_id=advisor).all()[:1][0]
        except:
            return None    
        return channel
    
    def get_all_channels(self,advisor):
        """    
                This method returns all channel for an advisor
             
        """
        try:
                channels = Channels.objects.filter(advisor_id=advisor).all()
                return channels
        except:
            return None
        return None
        
    def get_chat(self,chat_id):
        """    
                This method is used to get a channel (chat session) from chat id
            
        """
        try:
            channel = Channels.objects.filter(id=chat_id).all()[:1][0]
            return channel
        except :
            return None
        return None