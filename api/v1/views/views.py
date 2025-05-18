from django.core.exceptions import PermissionDenied
from django.db.models import Q
from rest_framework import viewsets, permissions
from django_filters import rest_framework as filters
from rest_framework.response import Response

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
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return ExchangeProposal.objects.filter(
            Q(ad_sender__user=self.request.user) |
            Q(ad_receiver__user=self.request.user)
        ).distinct()

    def perform_create(self, serializer):

        if serializer.validated_data['ad_sender'].user != self.request.user:
            raise PermissionDenied("Вы не владелец объявления-отправителя")
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user not in [instance.ad_sender.user, instance.ad_receiver.user]:
            raise PermissionDenied("У вас нет прав на изменение этого предложения")

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        if 'ad_sender' in request.data or 'ad_receiver' in request.data:
            raise PermissionDenied("Изменение объявлений запрещено")

        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.ad_sender.user != request.user:
            raise PermissionDenied("Только создатель предложения может его удалить")

        return super().destroy(request, *args, **kwargs)
