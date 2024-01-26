from rest_framework import serializers
from Accreditation.models import accreditation_records, program_accreditation
from Users.models import faculty_certificates

class AccreditationRecordSerializer(serializers.ModelSerializer):
    accredited_program = serializers.StringRelatedField(many=True)
    program_accreditation_level = serializers.StringRelatedField(many=True)

    class Meta:
        model = accreditation_records
        fields = ('program', 'instrument_level', 'description', 'status', 'due_date', 'survey_visit_date', 'accredited_program', 'program_accreditation_level')


class ProgramAccreditationSerializer(serializers.ModelSerializer):
    accredited_program = serializers.StringRelatedField(many=True)
    class Meta:
        model = program_accreditation

# class ProgramAccreditationSerializer(serializers.ModelSerializer):
#     accredited_program = serializers.StringRelatedField(many=True)
#     class Meta:
#         model = program_accreditation


# class AlbumSerializer(serializers.ModelSerializer):
#     tracks = serializers.StringRelatedField(many=True)

#     class Meta:
#         model = Album
#         fields = ['album_name', 'artist', 'tracks']
        
class FacultyCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = faculty_certificates
        fields = ('__all__')