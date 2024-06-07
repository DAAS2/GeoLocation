from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('register', views.register, name="register"),
    path('find_location', views.find_child, name='find_child'),
    path('contact_child', views.contact_child, name='contact_child'),
    path('save_child_location', views.save_child_location, name='save_child_location'),
    path('contact_child', views.contact_child, name="contct_child")
]
