
from django.conf.urls import include, url, patterns
import socketio.sdjango

socketio.sdjango.autodiscover()
from views import *
urlpatterns = patterns('',
    url(r'^account/(?P<pk>[0-9]+)/$', AccountDetail.as_view(), name='account_detail'),
    url(r'^account/create/$',AccountCreate.as_view(), name='account_create'), 
    
    url(r'^account/(?P<pk>[0-9]+)/update/$',AccountUpdate.as_view(),name='account_edit'),
    url(r'^account/(?P<pk>[0-9]+)/delete/$',
        AccountDelete.as_view(),
        name='account_delete'),
    url(r'^account/create/apartment/$',ApartmentCreate.as_view(), name='apartment_create'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'), 
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url("^socket\.io", include(socketio.sdjango.urls)),
	
    url(r'^like/$', like, name='like'),
    url("^create/$", create, name="create"),
    
    url("^$", rooms, name="rooms"),
    url("^(?P<slug>.*)$", room, name="room"),
)
