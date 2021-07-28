from django.urls import path

from teng import views

urlpatterns = [
    path('index/', views.index, name="index"),
    path('business/<int:id>', views.suppliers_with_business, name="suppliers_with_business"),
    path('subbus/<int:id>',views.suppliers_with_subbusiness,name="suppliers_with_subbusiness"),
    path('searchByKeyword/',views.search_by_keyword,name="search_by_keyword"),
    path('quickView/<int:id>',views.quick_view,name="quick_view")
]