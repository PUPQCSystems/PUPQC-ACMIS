from rest_framework import serializers
from .models import Programs

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programs
        fields = ('__all__')  
