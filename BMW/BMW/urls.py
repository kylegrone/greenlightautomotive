from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BMW.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^dealership/', include('dealership.urls', namespace="dealership")),
    url(r'^dealership/', include('dealership.urls', namespace='dealership' , app_name='dealership')),
    url(r'^livechat/', include('livechat.urls', namespace='livechat')),
    url(r'^customer/', include('customer.urls', namespace='customer')),
    url(r'^flagger/', include('flagging.urls', namespace='flagging')),
    url(r'^mobilecheckin/', include('mobilecheckin.urls', namespace='mobilecheckin' , app_name='mobilecheckin')),
    url(r'^admin/', include(admin.site.urls)),
#     url(r'^subview', include('subview.urls')),

# url(r'^oauth2/', include('oauth2_authentication.urls', namespace="oauth2"))
    
)
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
