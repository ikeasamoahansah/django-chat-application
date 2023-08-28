from django.urls import path
from . import views

urlpatterns = [
    path('', views.lobby, name='lobby'),
    path('create_room/', views.create_room, name="create_room"),
    path('room/<str:pk>', views.room, name="room"),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('logout', views.logout_view, name="logout")
]
