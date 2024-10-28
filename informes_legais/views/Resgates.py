from rest_framework import viewsets
from informes_legais.models.ResgateJcot import ResgatesJcot
from informes_legais.serializers import ResgatesJcotSerializer


class ResgatesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ResgatesJcot.objects.all()
    serializer_class = ResgatesJcotSerializer
