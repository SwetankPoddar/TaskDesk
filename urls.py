from django.conf.urls import url
from taskdesk import views


urlpatterns = [
	url(r'^login/$', views.user_login, name='login'),
]
