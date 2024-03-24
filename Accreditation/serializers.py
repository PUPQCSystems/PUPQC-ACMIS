from rest_framework import serializers
from .models import accredlevel, instrument, accredbodies
from Programs.serializers import ProgramSerializer


class AccredLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = accredlevel
        fields = ('__all__')  


class AccredbodiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = accredbodies
        fields = '__all__'

class InstrumentSerializer(serializers.ModelSerializer):
    # accredbodies = AccredbodiesSerializer(many=False)
    # program = ProgramSerializer(many=False, read_only = True)


    class Meta:
        model = instrument
        fields = '__all__'

  