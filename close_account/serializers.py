from rest_framework import serializers
from .models import CloseAccount


class CloseAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloseAccount
        fields = "__all__"
        read_only_fields = ['agent']