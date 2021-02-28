from . import views
from django.urls import path

urlpatterns = [
    path('', views.indexPage, name='indexPage'),
    path('qrcode', views.qrcode, name='qrcode'),
    path('registerpage', views.registerpage, name='registerpage'),
    path('officepage', views.officepage, name='officepage'),
    path('increment', views.increment, name='increment'),
    path('userinfo', views.userinfo, name='userinfo')
]