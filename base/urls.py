from django.urls import path
from django.contrib.auth.decorators import permission_required
from . import views


urlpatterns = [
    # path('', views.test, name="test"),
    path('abc/', views.abc, name="abc"),
    path('login/', views.loginPage, name="login"),
    path('viewdetails/<str:id>/', views.viewdetails, name="viewdetails"),
    # path('adminviewdetails/<str:id>/', views.adminviewdetails, name="adminviewdetails"),
    path('adminviewdetails/<int:id>/', views.adminviewdetails, name="adminviewdetails"),
    path('adminlogin/', views.adminloginPage, name="adminlogin"),
    # path('accounts/', include('django.contrib.auth.urls')),
   
    # path('adminregister/', views.adminregisterPage, name="adminregister"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('statusupdate/', views.statusupdate, name="statusupdate"),
    path('', views.home, name='home'),
    path('userdashboard/', views.userdashboard, name='userdashboard'),
    path('admindashboard/', views.admindashboard, name='admindashboard'),
    path('admin update password/', views.update_password1, name='admin update password'),
    path('lodgecomplaint/', views.lodge_complaint, name='lodgecomplaint'),
    path('updatepasswordUser/', views.update_password, name='updatepasswordUser'),
    path('pending',views.pending, name='pending'),
    path('inprocess',views.inprocess, name='inprocess'),
    path('closed',views.closed, name='closed'),
    path('total',views.total, name='total'),
    path('compStatusP/', views.complaint_status_Pending, name='complaint_status_P'),
    # path('compStatusP/<int:complaint_id>/', views.complaint_status_Pending, name='complaint_status_P'),

    path('compStatusS/', views.complaint_status_Solved, name='complaint_status_S'),
    path('compStatusIP/', views.complaint_status_InProcess, name='complaint_status_IP'),
    path('compStatusA/', views.complaint_status_All, name='complaint_status_A'),
    path('takeaction/', views.statusupdate, name='takeaction'),
]