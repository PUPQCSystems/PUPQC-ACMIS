from rest_framework import serializers
from Accreditation.models import accreditation_records, program_accreditation
from Users.models import CustomUser, category_training, faculty_certificates, seminar_workshop_training

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



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category_training
        fields = ('name',)


class WorkshopsSerializer(serializers.ModelSerializer):
    category_relation = serializers.StringRelatedField(many=False)

    class Meta:
        model = seminar_workshop_training
        fields = ('category', 'title', 'inclusive_date', 
                  'classification', 'sponsoring_agency', 
                  'created_by', 'created_at', 'modified_by', 
                  'modified_at', 'deleted_at', 'is_deleted', 'category_relation'
        )

