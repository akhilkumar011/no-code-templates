from django.urls import path
from .views import *

urlpatterns = [
    path('create_business/', create_business, name='create_business'),
    path('create/', create_module, name='create_module'),
    path('show/', show_modules, name='show_modules'),
    path('show/<str:module_id>/', get_module_data, name='edit_module'),
    path('edit/<str:module_id>/', edit_module, name='edit_module'),
    path('entry/<str:module_id>/', create_module_entry, name='create_module_entry'),
    path('entries/<str:module_id>/', view_entries, name='list_entries'),
    path('edit-entry/<str:module_id>/', update_module_entry, name='update_module_entry'),
    path('create-menu/', create_menu, name='create_menu'),
    path('menus/', get_menus, name='get_menu'),
]
