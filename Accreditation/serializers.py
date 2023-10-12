from rest_framework import serializers
from .models import accredtype, accredlevel


class AccredTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = accredtype
        fields = ('__all__')  


class AccredLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = accredlevel
        fields = ('__all__')  