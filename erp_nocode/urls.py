from django.urls import path
from .views import *

urlpatterns = [
    path('create_business/', create_business, name='create_business'),
    path('create/', create_module, name='create_module'),
    path('show/', show_modules, name='show_modules'),
    path('edit/<str:module_id>/', edit_module, name='edit_module'),
    path('entry/<int:module_id>/', create_module_entry, name='create_module_entry'),

]
