from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from informes_legais.serializers import DateRangeSerializer , AplicacoesSerializer
from informes_legais.models import AplicacoesJcot
from informes_legais.tasks.tasks import extrair_movimentacoes
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet , GenericViewSet
from informes_legais.models import AplicacoesJcot
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import viewsets


class GetMovimentosViewSet(viewsets.GenericViewSet):
    serializer_class = DateRangeSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            # print (serializer.data['data_inicio'])

            extrair_movimentacoes.delay(serializer.data['data_inicio'] , serializer.data['data_fim'])

            retorno  = {
                "message": "Dados enviados para Extração"
            }

            return Response(retorno, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AplicacoesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AplicacoesJcot.objects.all()
    serializer_class = AplicacoesSerializer



