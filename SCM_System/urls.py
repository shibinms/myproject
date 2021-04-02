from .import views
from django.urls import path

urlpatterns = [
    path('adm_login/', views.adm_login),
    path('adm_login_post/', views.adm_login_post),
    path('adm_add_branch/', views.adm_add_branch),
    path('adm_add_branch_post/', views.adm_add_branch_post),
    path('adm_add_manager/', views.adm_add_manager),
    path('adm_add_manager_post/', views.adm_add_manager_post),
    path('adm_add_product/', views.adm_add_product),
    path('adm_add_product_post/', views.adm_add_product_post),
    path('adm_add_raw_material/', views.adm_add_raw_material),
    path('adm_add_raw_material_post/', views.adm_add_raw_material_post),
    path('adm_allocate_raw_material/', views.adm_allocate_raw_material),
    path('adm_edit_branch/', views.adm_edit_branch),
    path('adm_edit_manager/', views.adm_edit_manager),
    path('adm_edit_product/', views.adm_edit_product),
    path('adm_edit_raw_material/', views.adm_edit_raw_material),
    path('adm_send_notification/', views.adm_send_notification),
    path('adm_send_notification_post/', views.adm_send_notification_post),
    path('adm_view_allocate_report/', views.adm_view_allocate_report),
    path('adm_view_branch/', views.adm_view_branch),
    path('adm_view_manager/', views.adm_view_manager),
    path('adm_view_material_allocated/', views.adm_view_material_allocated),
    path('adm_view_material_requested/', views.adm_view_material_requested),
    path('adm_view_notification/', views.adm_view_notification),
    path('adm_view_product/', views.adm_view_product),
    path('adm_view_production/', views.adm_view_production),
    path('adm_view_raw_material/', views.adm_view_raw_material),
    path('adm_view_request/', views.adm_view_request),
    path('adm_view_sales_details_admin/', views.adm_view_sales_details_admin),
    path('adm_view_sales_report_admin/', views.adm_view_sales_report_admin),
    path('adm_homepage/', views.adm_homepage)

]