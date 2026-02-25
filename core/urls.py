from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    # Chat APIs
    path('api/chat/', views.chat_api, name='chat_api'),
    path('api/chat/alert/', views.chat_alert, name='chat_alert'),
]


