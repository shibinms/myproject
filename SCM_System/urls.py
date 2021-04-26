from .import views
from django.urls import path
app_name="myapp"
urlpatterns = [
    path('lognindex/', views.lognindex),
    path('lognindex_post/', views.lognindex_post),
    path('adm_add_branch/', views.adm_add_branch),
    path('adm_add_branch_post/', views.adm_add_branch_post),
    path('adm_add_manager/', views.adm_add_manager),
    path('adm_add_manager_post/', views.adm_add_manager_post),
    path('adm_add_product/', views.adm_add_product),
    path('adm_add_product_post/', views.adm_add_product_post),
    path('adm_add_raw_material/', views.adm_add_raw_material),
    path('adm_add_raw_material_post/', views.adm_add_raw_material_post),
    path('adm_allocate_raw_material/', views.adm_allocate_raw_material),
    path('adm_send_notification/', views.adm_send_notification),
    path('adm_send_notification_post/', views.adm_send_notification_post),
    path('adm_view_allocate_report/', views.adm_view_allocate_report),
    path('adm_view_branch/', views.adm_view_branch,name="adm_view_branch"),
    path('adm_view_manager/', views.adm_view_manager,  name="adm_view_manager"),
    path('adm_view_material_allocated/', views.adm_view_material_allocated),
    path('adm_view_material_requested/', views.adm_view_material_requested),
    path('adm_view_notification/', views.adm_view_notification),
    path('adm_view_product/', views.adm_view_product,name="adm_view_product"),
    path('adm_view_production/', views.adm_view_production),
    path('adm_view_raw_material/', views.adm_view_raw_material,name="adm_view_raw_material"),
    path('adm_view_request/', views.adm_view_request),
    path('adm_view_sales_details_admin/', views.adm_view_sales_details_admin),
    path('adm_view_sales_report_admin/', views.adm_view_sales_report_admin),
    path('adm_homepage/', views.adm_homepage),
    path('adm_del_manager/<int:id>',views.adm_del_manager),
    path('adm_del_product/<int:id>',views.adm_del_product),
    path('adm_del_branch/<int:id>',views.adm_del_branch),
    path('adm_del_raw_material/<int:id>',views.adm_del_raw_material),
    path('adm_edit_branch/<int:id>',views.adm_edit_branch),
    path('adm_update_branch/',views.adm_update_branch),
    path('adm_edit_product/<int:id>',views.adm_edit_product),
    path('adm_update_product/',views.adm_update_product),
    path('adm_edit_raw_material/<int:id>',views.adm_edit_raw_material),
    path('adm_update_raw_material/',views.adm_update_raw_material),
    path('adm_edit_manager/<int:id>',views.adm_edit_manager),
    path('adm_update_manager/',views.adm_update_manager),
    path('adm_branch_name_search/',views.adm_branch_name_search),
    path('adm_manager_name_search/',views.adm_manager_name_search),
    path('adm_product_name_search/',views.adm_product_name_search),
    path('adm_raw_material_name_search/',views.adm_raw_material_name_search),
    path('sales_sales_entry/',views.sales_sales_entry),
    path('sales_sales_entry/',views.sales_sales_entry),
    path('sales_sales_entry_post/',views.sales_sales_entry_post),
    path('sales_del_cart/<int:id>',views.sales_del_cart),
    path('sales_view_sales_report_common/',views.sales_view_sales_report_common),
    path('sales_view_product_sales_staff/',views.sales_view_product_sales_staff),
    path('sales_view_profile/',views.sales_view_profile),
    path('sales_view_sales_details/<int:id>',views.sales_view_sales_details),
    path('sales_product_name_search/',views.sales_product_name_search),
    path('adm_notification_branch_name_search/',views.adm_notification_branch_name_search),
    path('adm_del_notification/<int:id>',views.adm_del_notification),
    path('production_home/',views.production_home),
    path('production_view_rawmaterial/',views.production_view_rawmaterial),
    path('production_update_material_usage/<int:id>',views.production_update_material_usage),
    path('production_update_material_usage_post/',views.production_update_material_usage_post),
    path('production_view_material_usage/',views.production_view_material_usage),
    path('production_update_production/',views.production_update_production),
    path('production_update_production_post/',views.production_update_production_post),
    path('production_view_production_report/',views.production_view_production_report),
    path('production_request_material_production/',views.production_request_material_production),
    path('production_product_name_search/',views.production_product_name_search),
    path('manager_home/',views.manager_home),
    path('manager_add_staff/',views.manager_add_staff),
    path('manager_add_staff_post/',views.manager_add_staff_post),
    path('manager_view_staff/',views.manager_view_staff),
    path('manager_edit_staff/<int:id>',views.manager_edit_staff),
    path('manager_update_staff/',views.manager_update_staff),
    path('manager_del_staff/<int:id>', views.manager_del_staff),
    path('manager_view_profile/', views.manager_view_profile),
    path('manager_view_products/', views.manager_view_products),
    path('manager_staff_name_search/', views.manager_staff_name_search),
    path('manager_product_name_search/', views.manager_product_name_search)


]