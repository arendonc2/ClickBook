from django.urls import path
from . import views

urlpatterns = [
    path('signupaccount/', views.signupaccount, name='signupaccount'),
    path('logout/', views.logoutaccount, name='logoutaccount'),
    path('login/', views.loginaccount, name = 'loginaccount'),
    path('reset_password_manual/', views.reset_password_manual, name='reset_password_manual'),
]
