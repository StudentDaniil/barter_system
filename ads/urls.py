from django.urls import path
from . import views

app_name = 'ads'

urlpatterns = [
    path('', views.AdListView.as_view(), name='list'),
    path('create/', views.AdCreateView.as_view(), name='create'),
    path('<int:pk>/', views.AdDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.AdUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.AdDeleteView.as_view(), name='delete'),
]
