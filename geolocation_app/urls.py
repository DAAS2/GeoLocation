from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('register', views.register, name="register"),
    path('update_location', views.update_location, name="update_location"),
    path('find_child', views.find_child, name='find_child'),
    path('contact_child', views.contact_child, name='contact_child')
]
