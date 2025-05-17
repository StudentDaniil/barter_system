from rest_framework import serializers
from models.models import Advertisement, ExchangeProposal


class AdSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Advertisement
        fields = '__all__'
        read_only_fields = ['user', 'created_at']


class ProposalSerializer(serializers.ModelSerializer):
    ad_sender = AdSerializer(read_only=True)
    ad_receiver = AdSerializer(read_only=True)

    class Meta:
        model = ExchangeProposal
        fields = '__all__'
        read_only_fields = ['created_at']

    def validate(self, data):
        if data['ad_sender'] == data['ad_receiver']:
            raise serializers.ValidationError("Cannot create proposal for the same ad")
        return data
