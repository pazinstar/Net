from django.urls import path
from .views import*
from . import views


app_name = 'balance'

urlpatterns = [
   
    path('', home, name='home'),

    path('balance/<str:username>/', show_balance, name='show_balance'),
     path('admin-login/', admin_login_view, name='admin_login'),
     path('Contact/', Contact_view, name='Contact'),
    path('deposit/', deposit, name='deposit'),
    path('login-admin/', loginadmin, name='loginadmin'),
    path('stkpush/', initiate_stk_push, name='initiate_stk_push'),
   path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('logout/', views.logoutadmin, name='logoutadmin'),
    path('process_stk_callback/', views.process_stk_callback, name='process_stk_callback'),

]