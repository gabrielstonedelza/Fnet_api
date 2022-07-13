from django.db.models import fields
from rest_framework import serializers
from .models import PaymentAtBank


class PaymentAtBankSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = PaymentAtBank
        fields = ['id', 'agent', 'username', 'teller_name', 'teller_phone', 'amount', 'total', 'd_200', 'd_100', 'd_50',
                  'd_20', 'd_10', 'd_5', 'd_2', 'd_1', 'date_added', 'time_added']
        read_only_fields = ['agent']

    def get_username(self, user):
        username = user.agent.username
        return username
