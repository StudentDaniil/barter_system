from rest_framework import serializers
from models.models import Advertisement, ExchangeProposal


class AdSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Advertisement
        fields = '__all__'
        read_only_fields = ['user', 'created_at']


class ProposalSerializer(serializers.ModelSerializer):
    ad_sender = serializers.PrimaryKeyRelatedField(
        queryset=Advertisement.objects.all(),
        error_messages={'does_not_exist': 'Объявление-отправитель не найдено'},
        required=False
    )
    ad_receiver = serializers.PrimaryKeyRelatedField(
        queryset=Advertisement.objects.all(),
        error_messages={'does_not_exist': 'Объявление-получатель не найдено'},
        required=False
    )
    status = serializers.ChoiceField(
        choices=ExchangeProposal.STATUS_CHOICES,
        default='pending',
        required=False
    )

    class Meta:
        model = ExchangeProposal
        fields = '__all__'
        read_only_fields = ['created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.context.get('request') and self.context['request'].method in ['PATCH', 'PUT']:
            self.fields['ad_sender'].read_only = True
            self.fields['ad_receiver'].read_only = True

    def validate(self, data):

        if self.context['request'].method == 'POST':
            if not data.get('ad_sender') or not data.get('ad_receiver'):
                raise serializers.ValidationError("Оба объявления должны быть указаны")

            if data['ad_sender'] == data['ad_receiver']:
                raise serializers.ValidationError("Нельзя создать предложение для одного объявления")

            if data['ad_sender'].user == data['ad_receiver'].user:
                raise serializers.ValidationError("Нельзя отправлять предложение самому себе")

        return data
