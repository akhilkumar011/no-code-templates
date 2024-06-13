# api/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from api.views.erp_data_utility_view import get_erp_utility_data, get_data_columns,ConfigDataView
from api.views.views import HbAppEntityViewSet, MasterView


# app_name = "api"
router = DefaultRouter()
router.register(r'appentity', HbAppEntityViewSet)
urlpatterns = [

                  path('txnData/', get_erp_utility_data, name='erp_utility_data'),
                  path('txnData/<str:data_code>', get_erp_utility_data, name='erp_utility_data'),
                  path('config_data/', get_data_columns, name='data_columns'),
                  path('erp/master/', MasterView.as_view()),
                  path('save-config/', ConfigDataView.as_view(), name='save-config'),
              ] + router.urls
