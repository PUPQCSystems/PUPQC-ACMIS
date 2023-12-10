from rest_framework import serializers
from .models import accredtype, accredlevel, instrument


class AccredTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = accredtype
        fields = ('__all__')  


class AccredLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = accredlevel
        fields = ('__all__')  


class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = instrument
        fields = ('name', 'description', 'accredbodies')