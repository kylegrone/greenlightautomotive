
from django.conf.urls import url

from . import views


urlpatterns = [
    #url(r'^$', views.IndexView.as_view(), name='index'),  
    url(r'^$', views.index, name='index'),   
     url(r'^upload$', views.upload, name='upload'),    
      url(r'^addchannel', views.addchannel, name='addchannel'),   
      url(r'^deletechannel', views.deleteChannel, name='deletechannel'),  
]