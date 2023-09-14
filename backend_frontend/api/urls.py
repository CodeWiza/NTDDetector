from django.urls import path
from .views import *

urlpatterns = [
    path('create', create_user, name='create_user'),
    path('',index, name='index'),
    path('dashboard',dashboard),
    path('prediction_form', prediction_form, name='prediction_form'),
    path('prediction_form/save', save_data, name='save_data'),
]
