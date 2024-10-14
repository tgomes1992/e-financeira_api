from django.http import HttpResponse
from django.views import View
from django.shortcuts import render , redirect
from ..forms import ArquivosForm
from io import BytesIO
import pandas as pd
from ..validacao_5401 import XML_5401
from s3management.views import S3ManagementClient
from django.contrib import messages
from ..tasks import analise_5401

class View_5401(View):

    template_name = "informes_legais/analise_5401.html"
    form = ArquivosForm()

    def get(self, request):
        context = {
            "form": self.form,
        }

        return render(request ,self.template_name , context)

    def post(self , request):
        filename = "analise_5401.xlsx"
        arquivo = request.FILES['arquivo']

        client = S3ManagementClient()
        client.upload_unique(key=arquivo.name , body=arquivo)


        analise_5401.delay(arquivo.name)


        # async_task('informes_legais.tasks.analise_5401' , arquivo.name)
        messages.success(request, 'Relatório Enviado para conferência, após finalizado será disponibilzado na tela de arquivos')

        return redirect('5401')
