from . import views
from django.urls import include,path
from django.contrib import admin
urlpatterns=[
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('landing', views.landing, name='landing'),
    path('adminlogin',views.adminlogin,name='adminlogin'),
    path('transaction',views.transaction,name='transaction'),
    path('demo',views.demo,name="demo"),
    path('dash',views.dash,name="dash"),
    path('subscribe',views.subscribe,name="subscribe"),
]