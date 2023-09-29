from django.urls import path
from .views import *

urlpatterns = [
    path('signup', create_user, name='create_user'),
    path('signin', login_user, name='find_user'),
    path('',login, name='login'),
    path('dashboard',dashboard,name='display_dashboard'),
    path('prediction_form', prediction_form, name='prediction_form'),
    path('prediction_form/save', save_data, name='save_data'),
    path('logout',logout_user,name="logout"),
    
]
