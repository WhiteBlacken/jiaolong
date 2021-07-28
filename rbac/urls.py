from django.urls import path

from rbac import views

urlpatterns = [
    path('goCreateAcc/',views.goCreateAcc,name="goCreateAcc"),
    path('info_of_myaccount/',views.info_of_myaccount,name="info_of_myaccount"),
    path('upgrade_by_spend/',views.upgrade_by_spend,name="upgrade_by_spend")

]