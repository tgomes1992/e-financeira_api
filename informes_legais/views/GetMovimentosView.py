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


class GetMovimentacoes(viewsets.ViewSet):

    @swagger_auto_schema(
        operation_description="Extract movimentacoes within a specified date range.",
        request_body=DateRangeSerializer,
        responses={
            200: openapi.Response(
                description="Successfully received dates for processing",
                examples={
                    "application/json": {
                        "message": "Dates received successfully!",
                        "start_date": "2024-01-01",
                        "end_date": "2024-01-31"
                    }
                }
            ),
            400: "Validation error"
        },
        tags=["Extrações"]
    )
    @action(detail=False, methods=['post'])
    def extrair_movimentacoes(self, request):
        serializer = DateRangeSerializer(data=request.data)

        if serializer.is_valid():
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']

            # Trigger Celery task
            extrair_movimentacoes.delay(start_date, end_date)

            # Response indicating dates received successfully
            return Response(
                {"message": "Dates received successfully!", "start_date": start_date, "end_date": end_date},
                status=status.HTTP_200_OK
            )

        # Return errors if validation fails
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AplicacoesViewSet(generics.ListAPIView):


    queryset = AplicacoesJcot.objects.all()
    serializer_class  = AplicacoesSerializer

