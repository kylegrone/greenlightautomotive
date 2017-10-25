from django.conf.urls import url

# from . import views
from flagging.views import  flagging_app,login,media,action_plan,reports,techview,inspection
# from flagging.views import login
# import views.login
# import views.flagging_app
# import views.techview
# import views.inspection
# import views.media
# import views.action_plan
# import views.reports
# from flagging import views.login
urlpatterns = [
     url(r'^$', flagging_app.index, name='index'),   
     url(r'^login/(?P<dealer_code>[a-zA-Z0-9_-]+)/?$', login.loginview, name='login'),     
    url(r'^login/$', login.loginview, name='login'),
    url(r'^logout/$', login.logoutview, name='logout'),
    url(r'^password/change$', login.passchange, name='passchange'),
    url(r'^password/create$', login.passcreate, name='passcreate'),
    url(r'^password/reset$', login.passreset, name='passreset'),
    url(r'^terms/$', login.terms, name='terms'),
    url(r'^username/reset$', login.userreset, name='userreset'),
    url(r'^firstlogin/$', login.firstlogin, name='firstlogin'),
    url(r'^newuser/$', login.newuser, name='newuser'),
    url(r'^tempnum/$', login.addTempNumber, name='tempnum'),
    url(r'^confirmation/$', login.confirmation, name='confirmation'),
    url(r'^ro_list/$', flagging_app.ro_list_ajax, name='ro_list'),
    url(r'^search_ros/$', flagging_app.search_ros_ajax, name='search_ros'),
    url(r'^update_flags/$', flagging_app.update_flags, name='update_flags'),
    url(r'^shop_notes/$', flagging_app.get_shop_notes, name='shop_notes'),
#     url(r'^shop_notes_ajax/$', views.flagging_app.get_shop_notes_by_filter, name='shop_notes_ajax'),
    url(r'^add_note/$', flagging_app.add_note, name='add_note'),
    url(r'^tech_view/$', techview.tech_view, name='tech_view'),
    url(r'^inspection/$', inspection.inspection, name='inspection'),
    url(r'^inspection/pdf$', inspection.get_results_summary_pdf, name='inspection_pdf'),
    url(r'^media/$', media.media, name='media'),
    url(r'^delete_media/$', media.delete_media, name='delete_media'),
    url(r'^result_summary/$', inspection.get_results_summary, name='result_summary'),
    url(r'^add_inspection_record/$', inspection.add_inspection_record, name='add_inspection_record'),
    url(r'^action_plan/$', action_plan.action_plan, name='action_plan'),
    url(r'^ro_details/$', flagging_app.get_ro_details_ajax, name='ro_details'),
    url(r'^reports/$', reports.get_reports, name='reports'),
    url(r'^reports/flag_analysis$', reports.get_shop_flag_report, name='flag_analysis'),
    url(r'^get_flag_notes$', flagging_app.get_flag_notes, name='get_flag_notes'),
    url(r'^add_recommendations$', flagging_app.add_recommendations, name='add_recommendations'),
    url(r'^inspection_test$', inspection.inspection_test, name='inspection_test'),
    url(r'^edit_recommendation', techview.edit_recommendation, name='edit_recommendation'),
    url(r'^mark_ro_complete', flagging_app.mark_as_complete, name='mark_ro_complete'),
    url(r'^get_repair_order_list', reports.get_repair_order_list, name='get_repair_order_list'),
    url(r'^generatepdf', action_plan.generate_pdf_view, name='generatepdf'),
    url(r'^action_plan_pdf', action_plan.action_plan_pdf, name='action_plan_pdf'),
    url(r'^email_action_plan', action_plan.email_action_plan, name='email_action_plan'),
    url(r'^reports/generate_report$', reports.generate_report, name='generate_report'),
]