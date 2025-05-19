from django.urls import path
from .views import (ProposalListView, ProposalDetailView, ProposalCreateView, ProposalUpdateView, ProposalDeleteView)

app_name = 'proposals'

urlpatterns = [
    path('', ProposalListView.as_view(), name='list'),
    path('create/', ProposalCreateView.as_view(), name='create'),
    path('<int:pk>/', ProposalDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', ProposalUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', ProposalDeleteView.as_view(), name='delete'),
]
