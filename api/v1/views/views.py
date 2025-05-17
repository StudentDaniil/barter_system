from rest_framework import viewsets, permissions
from django_filters import rest_framework as filters
from models.models import Advertisement, ExchangeProposal
from api.v1.serializers.serializers import AdSerializer, ProposalSerializer
from .permissions import IsOwnerOrReadOnly


class AdvertisementFilter(filters.FilterSet):
    class Meta:
        model = Advertisement
        fields = {
            'category': ['exact'],
            'condition': ['exact'],
            'user': ['exact'],
            'created_at': ['gte', 'lte'],
        }


class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdSerializer
    filterset_class = AdvertisementFilter
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExchangeProposalFilter(filters.FilterSet):
    class Meta:
        model = ExchangeProposal
        fields = {
            'status': ['exact'],
            'ad_sender': ['exact'],
            'ad_receiver': ['exact'],
            'created_at': ['gte', 'lte'],
        }


class ExchangeProposalViewSet(viewsets.ModelViewSet):
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = ExchangeProposalFilter

    def get_queryset(self):
        return ExchangeProposal.objects.filter(
            ad_sender__user=self.request.user
        ) | ExchangeProposal.objects.filter(
            ad_receiver__user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
