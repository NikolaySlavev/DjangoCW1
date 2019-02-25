from django.urls import path, include
from . import views

urlpatterns = [
	path('api/getstories/', views.post_list, name='post_list'),
	path('api/login/', views.handle_login, name='login'), #include('django.contrib.auth.urls')),
	path('api/logout/', views.handle_logout, name='logout'),
	path('api/poststory/', views.post_new, name='post_new'),
	path('api/deletestory/', views.post_remove, name='post_remove'),
]