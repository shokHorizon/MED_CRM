from django.urls import path

from . import views

urlpatterns = [
    path('<str:pk>/tasks/', views.tasks, name='tasks'),
    path('<str:pk>/storage/', views.storage, name='storage'),
    path('<str:pk>/partners/', views.partners, name='partners'),
    path('<str:pk>/partners/<int:id>/', views.clients, name='clients'),
    path('<str:pk>/', views.clinic, name='clinic'),
    path('', views.index, name='home'),
]
