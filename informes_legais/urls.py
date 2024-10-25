# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from informes_legais.views.GetMovimentosView import GetMovimentacoes , AplicacoesViewSet

router = DefaultRouter()
router.register('movimentos', GetMovimentacoes, basename='get_movimentacoes')



urlpatterns = [
    path('', include(router.urls)),
    path("aplicacoes" , AplicacoesViewSet.as_view(), name="aplicacoes"),
]