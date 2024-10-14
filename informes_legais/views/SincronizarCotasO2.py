from django.http import HttpResponse
from django.views import View
from django.shortcuts import render , redirect
from ..forms import ArquivosForm , SincronizarCotas
from io import BytesIO
import pandas as pd
from ..validacao_5401 import XML_5401
from s3management.views import S3ManagementClient
# from django_q.tasks import async_task
from django.contrib import messages
from ..tasks import analise_5401 , SincronizarCotasO2

class SincronizarCotas(View):

    template_name = "informes_legais/SincronizarCotasO2.html"

    def get(self, request):


        return render(request ,self.template_name )

    def post(self , request):

        SincronizarCotasO2.delay(request.POST['data'])

        messages.success(request, 'Sincronização Iniciada')

        return redirect('sincronizarCotas')
