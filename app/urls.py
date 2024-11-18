from django.urls import path
from .views import *
urlpatterns = [

    path('register/', register_admin, name='admin_register'),
    path('login/', login_admin, name='admin_login'),
    path('logout/', logout_admin, name='logout_admin'),
    # path('', first_page, name='first_page' ),
    # path('products/<int:client_id>/', second_page, name='second_page'),
    # path('second-page/<int:client_id>/',second_page, name='second_page_with_id'),
    path('', second_page, name='second_page'),
    path('client-requests/', view_client_requests, name='view_client_requests'),
    path('client_details/<int:client_id>/', client_details, name='client_details'),
    path('delete-client/<int:client_id>/', delete_client, name='delete_client'),
    # path('send-email/<int:client_id>/', send_email, name='send_email'),
    path('add-product/', add_product, name='add_product'),
    path('edit-product/<int:product_id>/', edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', delete_product, name='delete_product'),
    path('product_list', product_list, name='product_list'),
    path('marble/<int:client_id>/', marble, name='marble'),
    path('welcome/<int:client_id>/', welcome, name='welcome'),
    path('agreement/<int:client_id>/', agreement, name='agreement'),
    path('success/', success, name='success'),
    path('special-client/', special_client, name='special_client'),

]
