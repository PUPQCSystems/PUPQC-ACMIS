from rest_framework import serializers
from .models import accredtype


class AccredTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = accredtype
        fields = ('__all__')  