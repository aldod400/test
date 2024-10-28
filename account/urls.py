from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name = 'register'),
    path('profile', views.profile, name = 'profile'),
    path('login', views.login, name = 'login'),
    path('logout', views.logout, name = 'logout'),
    path('profile/<str:id>', views.profile_by_id, name = 'profile_by_id'),
    path('forget_password', views.forget_password, name = 'forget_password'),
]