from django.conf.urls import url
from taskdesk import views


urlpatterns = [
	url(r'^$', views.redirectToLogin),
	url(r'^about-us/$', views.about_us, name='about_us'),
	url(r'^faq/$', views.faq, name='faq'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^register/$', views.register, name='register'),
	url(r'^logout/$', views.user_logout, name='user_logout'),
	url(r'^tasks/$', views.view_tasks, name ='view_tasks'),
	url(r'^tasks/category/(?P<category_id>\d+)/$', views.view_tasks, name ='view_tasks'),
	url(r'^tasks/create/$', views.createTask, name ='createTask'),
	url(r'^tasks/edit/(?P<task_id>\d+)/$', views.editTask, name ='editTask'),
	url(r'^tasks/manage$', views.manageTasks, name ='manageTasks'),
	url(r'^categories/$', views.view_categories, name = 'view_categories'),
	url(r'^categories/create$', views.createCategory, name = 'createCategory'),
	url(r'^categories/edit/(?P<category_id>\d+)/$', views.editCategory, name ='editCategory'),
	url(r'^settings/$', views.userPersonalizeSettings, name='userPersonalizeSettings'),
	url(r'^settings/account$', views.userAccountSettings, name='userAccountSettings'),
	url(r'^settings/account/change-password$', views.userChangePassword, name='userChangePassword'),
	url(r'^settings/account/delete$', views.userDeleteAccount, name='userDeleteAccount'),
#ACTION RELATED URLS
	url(r'^tasks/delete/(?P<task_id>\d+)/$', views.deleteTask, name ='deleteTask'),
	url(r'^tasks/done/(?P<task_id>\d+)/$', views.markAsDoneTask, name ='markAsDoneTask'),
	url(r'^tasks/notDone/(?P<task_id>\d+)/$', views.markAsNotDone, name ='markAsNotDone'),
	url(r'^categories/delete/(?P<category_id>\d+)/$', views.deleteCategory, name ='deleteCategory'),
]
