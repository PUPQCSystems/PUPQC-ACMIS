from rest_framework import serializers
from Accreditation.models import accreditation_records, program_accreditation

class AccreditationRecordSerializer(serializers.ModelSerializer):
    accredited_program = serializers.StringRelatedField(many=True)
    class Meta:
        model = program_accreditation
        fields = ('program', 'instrument_level', 'description', 'status', 'due_date', 'survey_visit_date', 'accredited_program')