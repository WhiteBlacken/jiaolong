from django.urls import path

from teng import views

urlpatterns = [
    path('index/', views.index, name="index"),
    path('business/<int:id>', views.suppliers_with_business, name="suppliers_with_business"),
    path('subbus/<int:id>',views.suppliers_with_subbusiness,name="suppliers_with_subbusiness"),
    path('searchByKeyword/',views.search_by_keyword,name="search_by_keyword"),
    path('quickView/<int:id>',views.quick_view,name="quick_view"),
    path('show_supply_detail/<int:id>',views.show_supply_detail,name="show_supply_detail"),
    # 之前的searchByKeyword是通过表单提交，在supplier的详细信息中不好通过表单提交，暂时再写一个方法
    path('search_by_keyword1/<str:searchText>',views.search_by_keyword1,name="search_by_keyword1")
]