from django.conf.urls import url

from customer.views import login, main, vehicle, account, notifications, appoint, service , statusalert,cart


urlpatterns = [  
    url(r'^$', login.login, name='index'),
#     url(r'^import_csv$', login.import_csv, name='index'),
    url(r'pull_models', login.pull_models, name='pull_models'),
    url(r'create_models', login.create_models, name='create_models'),
    url(r'delete_models', login.delete_models, name='delete_models'),
    url(r'create_models', login.create_models, name='create_models'),
    url(r'^login/(?P<dealer_code>[a-zA-Z0-9_-]+)/?$', login.login, name='login'),
    url(r'^login/?$', login.login, name='login'),
    url(r'^password/reset/$', login.passreset, name='passreset'),
    url(r'^username/reset/$', login.userreset, name='userreset'),
    url(r'^password/create$', login.passcreate, name='passcreate'),
    url(r'^main/$', vehicle.mainview , name='main'),
    url(r'^accountsettings/$', account.accountview , name='accountsettings'),
    url(r'^logout/$', login.logout, name='logout'),
    url(r'^test_ocr/$', main.test_ocr, name='test_ocr'),
    url(r'^puller/$', main.test_puller, name='puller'),
    url(r'^vehichlewidget/$', vehicle.get_vehicle, name='vehichlewidget'),
    url(r'^delete_vehicle/$', vehicle.del_vehicle, name='del_vehicle'),
    url(r'^ocr_snap/$', vehicle.ocr_snap, name='ocr_snap'),
    url(r'^delete_account/$', account.delete, name='delete_account'),
    url(r'^notifications/$', notifications.notificationssettings, name='notifications'),
    url(r'^findapp/$', appoint.find_exiting_appointment, name='findapp'),
    url(r'^search_app/$', appoint.search_app, name='search_app'),#used for searching thourhg ajax
    url(r'^new_customer_vehicle/$', login.new_customer_vehicle, name='new_customer_vehicle'),
    url(r'^vehicle_selection_appointment/$', appoint.vehicle_selection, name='vehicle_selection_appointment'),
    url(r'^service_selection_appointment/$', appoint.service_selection_appointment, name='service_selection_appointment'),
    url(r'^date_selection_appointment/$', appoint.date_selection_appointment, name='date_selection_appointment'),
    url(r'^get_all_services_ajax/$', service.get_all_services, name='get_all_services_ajax'),
    url(r'^save_appointment_services_ajax/$', service.save_all_services, name='save_appointment_services_ajax'),
    url(r'^get_all_advisors_ajax/$', service.get_all_advisor, name='get_all_advisors_ajax'),
    url(r'^save_advisor_ajax/$', service.save_advisor, name='save_advisor_ajax'),
    url(r'^schedule_appointment/$', appoint.schedule_appointment, name='schedule_appointment'),
    url(r'^cancel_appointment/$', appoint.cancel_appointment, name='cancel_appointment'),          
     url(r'^search_by_code_phone/$', appoint.search_by_code_phone, name='search_by_code_phone'),
     url(r'^book_appointment/$', appoint.book_appointment, name='book_appointment'),
     url(r'^check_username_exist/$', login.check_username, name='check_username'),
    url(r'^createuser/$', login.createuser, name='createuser'),
     url(r'^registeruer/$', login.registeruer, name='registeruer'),
    url(r'^sendemail/$', appoint.sendemail, name='sendemail'),
    url(r'^testingurl/$', login.testing, name='testingurl'),
     url(r'^uploadvin/$', appoint.uploadvin, name='uploadvin'),
     url(r'^book_appointment_now_new/$', appoint.book_appointment_now_new, name='book_appointment_now_new'),
     url(r'^book_appointment_now_existing/$', appoint.book_appointment_now_existing, name='book_appointment_now_ext'),
      url(r'^get_available_slabs_for_date/$', appoint.get_available_slabs_for_date, name='get_available_slabs_for_date'),
      url(r'^check_userprofile/$', appoint.check_userprofile, name='check_userprofile'),
      url(r'^get_available_adivsors_for_date/$', appoint.get_available_adivsors_for_date, name='get_available_adivsors_for_date'),
      url(r'^save_appointment_now_ext/$', appoint.save_appointment_now_ext, name='save_appointment_now_ext'),
      url(r'^statusalert/(?P<appointment_id>\d+)/$', statusalert.index, name='status_alert_index'),
      
       url(r'^approvestatus/(?P<appointment_id>\d+)/$', statusalert.approve_recomandations, name='approve_status'),
       
       url(r'^replystatus/(?P<appointment_id>\d+)/$', statusalert.reply, name='reply_status'),

        url(r'^getcart/$', cart.get_cart, name='getcart'),
    url(r'^send_activation_code/$', service.send_activation_code, name='send_activation_code'),
     url(r'^save_customer_number/$', service.save_customer_number, name='save_customer_number'),

       url(r'^paymentstatus/(?P<appointment_id>\d+)/$', statusalert.payment, name='payment_status'),
       url(r'^getcart/$', cart.get_cart, name='getcart'),
        url(r'^download_calendar/$', appoint.download_calendar, name='download_calendar'),
        url(r'^sync_gcalendar/$', login.sync_gcalendar, name='sync_gcalendar'),
  
        url(r'oauth2callback', login.auth_return, name='return'),
        url(r'print_appointment', appoint.print_appointment, name='print_appointment'),
        url(r'^service_history/(?P<vehicle_id>[a-zA-Z0-9_-]+)/?$', vehicle.service_history, name='service_history'),
         url(r'^(?P<dealer_code>[a-zA-Z0-9_-]+)/?$', login.index, name='index'), 
        
   
   
]