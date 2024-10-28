# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from informes_legais.views.GetMovimentosView import GetMovimentosViewSet , AplicacoesViewSet
from informes_legais.views.Resgates import ResgatesViewSet

router = DefaultRouter()
router.register('extrair_movimentos', GetMovimentosViewSet, basename='get_movimentacoes')
router.register('Aplicacoes', AplicacoesViewSet, basename='aplicacoes')
router.register('Resgates', ResgatesViewSet, basename='resgates')


urlpatterns = [
    path('', include(router.urls)),

]