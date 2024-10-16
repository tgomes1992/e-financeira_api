from django.db import models
from datetime import datetime

class MovimentoDetalhado(models.Model):
    notaOperacao = models.CharField(max_length=100)
    notaAplicacao = models.CharField(max_length=100)
    dsFormaLiquidacao = models.CharField(max_length=100)
    tpLiquidacao = models.CharField(max_length=100)
    dsContaLiquidacao = models.CharField(max_length=100)
    qtdCotas = models.FloatField()
    vlOriginal = models.FloatField()
    vlOperacao = models.FloatField()
    vlIR = models.FloatField()
    vlPenaltyFee = models.FloatField()
    vlReceitaSaqueCarencia = models.FloatField()
    vlIOF = models.FloatField()
    vlLiquido = models.FloatField()
    data = models.DateTimeField(default=datetime(2099,12,31))
    cotista = models.CharField(max_length=14  ,  default="")

    @classmethod
    def from_dict(cls, data):
        return cls(**data)