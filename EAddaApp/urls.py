from django.urls import path
from . import views
urlpatterns = [
	path('', views.adminLogin, name="admin_login"),
	path('check_for_login', views.checkForLogin, name='check_for_login'),
	path('admin_home', views.adminHome, name="admin_home"),

	path('driver', views.drivers, name='drivers'),
	path('available_drivers', views.available_drivers, name='available_drivers'),
	path('ride_request', views.ride_request, name='ride_request'),
	# path('delete_object/<str:id>', views.delete_object, name='delete_object'),
	path('logout', views.logout, name='logout'),
]