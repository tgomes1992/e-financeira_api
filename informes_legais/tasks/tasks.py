from informes_legais.ControllersEfinanceira import ExtratorMovimentacoes
from celery import shared_task


@shared_task
def extrair_movimentacoes(data_inicial , data_final):
    extrator = ExtratorMovimentacoes()
    extrator.main_extrair_movimentacoes(data_inicial , data_final)
