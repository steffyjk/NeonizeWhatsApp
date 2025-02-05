from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('chat/<str:chat_id>/', views.chat_detail, name='chat_detail'),
]
