from django.urls import path

from myAdmin import views

urlpatterns = [
    # 首页
    path('', views.index, name="adminIndex"),
    # 供应商
    path('show_supply_table/', views.show_supply_table, name="show_supply_table"),
    path('delete_supplier/<int:id>', views.delete_supplier, name="delete_supplier"),
    path('go_edit_supplier/<int:id>', views.go_edit_supplier, name="go_edit_supplier"),
    path('update_supplier/', views.update_supplier, name="update_supplier"),
    # 关键词
    path('show_keyword_table/', views.show_keyword_table, name="show_keyword_table"),
    path('delete_keyword/<int:id>', views.delete_keyword, name="delete_keyword"),
    path('go_add_keyword', views.go_add_keyword, name="go_add_keyword"),
    path('go_edit_keyword/<int:id>', views.go_edit_keyword, name="go_edit_keyword"),
    path('add_keyword', views.add_keyword, name="add_keyword"),
    path('update_keyword', views.update_keyword, name="update_keyword"),
    path('unsave_keyword', views.unsave_keyword, name="unsave_keyword"),
    path('go_view_keyword/<int:id>', views.go_view_keyword, name="go_view_keyword"),
    # 中英同义词
    path('show_keyword_similar_cn_table/', views.show_keyword_similar_cn_table, name="show_keyword_similar_cn_table"),
    path('show_keyword_similar_en_table/', views.show_keyword_similar_en_table, name="show_keyword_similar_en_table"),
    path('delete_keyword_cn/<int:id>', views.delete_keyword_cn, name="delete_keyword_cn"),
    path('delete_keyword_en/<int:id>', views.delete_keyword_en, name="delete_keyword_en"),
    path('go_edit_keyword_cn/<int:id>', views.go_edit_keyword_cn, name="go_edit_keyword_cn"),
    path('go_edit_keyword_en/<int:id>', views.go_edit_keyword_en, name="go_edit_keyword_en"),
    path('unsave_keyword_cn/', views.unsave_keyword_cn, name="unsave_keyword_cn"),
    path('unsave_keyword_en', views.unsave_keyword_en, name="unsave_keyword_en")

]
