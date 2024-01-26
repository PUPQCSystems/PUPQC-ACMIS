from rest_framework import generics, serializers
from Accreditation.models import accreditation_records, program_accreditation
from Users.models import faculty_certificates
from .serializers import AccreditationRecordSerializer, FacultyCertificateSerializer

class AccreditationRecords(generics.ListAPIView):
    queryset = accreditation_records.objects.select_related().filter(is_deleted=False)
    serializer_class = AccreditationRecordSerializer


class FacultyCertificateRecords(generics.ListAPIView):
    queryset = faculty_certificates.objects.filter(is_deleted=False)
    serializer_class = FacultyCertificateSerializer