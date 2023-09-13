from django.urls import path
from .views import *

urlpatterns = [
    path('create', create_user, name='create_user'),
    path('', home, name='home'),
    path('dashboard',dashboard),
    path('prediction_form', prediction_form, name='prediction_form'),
    path('prediction_form/save', save_data, name='save_data'),
    path('logout', logout_user, name='logout'),     
]
