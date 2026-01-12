from django.urls import path
from . import views
from .logic import model_permissions_settings, access_denied

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('add/user/', views.add_user,  name='add_user'),
    path('edit/user/<str:user_id>/', views.edit_user, name='edit_user'),
    path('delete/user/<str:user_id>/', views.delete_user, name='delete_user'),
    path('roles/', views.role_list, name='role_list'),
    path('add/role/', views.add_role, name='add_role'),
    path('edit/role/<str:role_id>/', views.edit_role, name='edit_role'),
    path('delete/role/<str:role_id>/', views.delete_role, name='delete_role'),
    path('default/passwords/', views.password_list, name='password_list'),
    path('add/defult/password/', views.add_password, name='add_password'),
    path('sign-in/', views.login_view, name='login'),
    path('change/password/<str:user_id>/', views.change_password, name='change_password'),
    path('change/new_password/<str:user_id>/', views.new_change_password, name='new_change_password'),
    path('sign/out/', views.logout_view, name='logout'),
    path("forgot-password/", views.forgot_password_view, name="forgot_password"),
    path("reset-password/<uidb64>/<token>/<expiry_data>/", views.recover_password_view, name="recover_password"),
    path('role/permissions/settings/<str:role_id>/', model_permissions_settings, name='model_permissions_settings'),
    path('access/denied/<str:message>/', access_denied, name='access_denied')
]
