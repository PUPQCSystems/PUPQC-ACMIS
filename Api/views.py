from rest_framework import generics, serializers
from Accreditation.models import accreditation_records, program_accreditation
from Users.models import category_training, faculty_certificates, seminar_workshop_training
from .serializers import AccreditationRecordSerializer, CategorySerializer, FacultyCertificateSerializer, WorkshopsSerializer

class AccreditationRecords(generics.ListAPIView):
    queryset = accreditation_records.objects.select_related().filter(is_deleted=False)
    serializer_class = AccreditationRecordSerializer


class FacultyCertificateRecords(generics.ListCreateAPIView):
    queryset = faculty_certificates.objects.filter(is_deleted=False)
    serializer_class = FacultyCertificateSerializer


class SeminarRecords(generics.ListCreateAPIView):
    queryset = seminar_workshop_training.objects.filter(is_deleted=False)
    serializer_class = WorkshopsSerializer

class CreateCategory(generics.ListCreateAPIView):
    queryset = category_training.objects.filter(is_deleted=False)
    serializer_class = CategorySerializer