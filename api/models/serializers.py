# serializers.py

from rest_framework import serializers
from .models import HbAppEntity


class HbAppEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = HbAppEntity
        fields = '__all__'
