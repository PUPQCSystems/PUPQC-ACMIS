from rest_framework import generics, serializers
from Accreditation.models import accreditation_records, program_accreditation
from .serializers import AccreditationRecordSerializer

class ItemListCreateView(generics.ListAPIView):
    queryset = program_accreditation.objects.select_related('program','instrument_level').filter(is_deleted=False)
    serializer_class = AccreditationRecordSerializer