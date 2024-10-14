
from .validacao_5401 import XML_5401
from s3management.views import S3ManagementClient
from io import BytesIO , StringIO
from datetime import datetime
import os
import csv
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from celery import shared_task
import subprocess
from .Controllers5401.ExtratorCotasJcot import ExtratorCotas
from intactus.osapi import o2Api
import os
import pandas as pd




@shared_task
def timeConsumingtask():


    emails = ['"thiago.conceicao@oliveiratrust.com.br"']

    output = StringIO()
    writer = csv.writer(output)

    # Reset the file pointer to the beginning of the file
    output.seek(0)


    result = subprocess.run(f'px aux', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    lines = result.stdout.strip().split('\n')





    email = EmailMessage("Leitura Servidor", "Isso é um teste", "thiago.conceicao@oliveiratrust.com.br", emails)
    email.attach('ps_aux.txt', output.getvalue(), 'text/csv')
    email.send()

    return {"nome": "bg task", "message": "email enviado"}


@shared_task
def analise_5401(file_key):
    arquivo_bite = BytesIO()
    s3client = S3ManagementClient()
    arquivo = s3client.client.get_object(Bucket=s3client.bucket_name, Key=file_key)
    xml = XML_5401(arquivo['Body'])
    xml.gerar_arquivo_validacao(arquivo_bite)
    arquivo_bite.seek(0)
    s3client.upload_unique(f"analise_5401_{datetime.now().strftime('%d%m%Y_%H%M%S')}.xlsx" , arquivo_bite.read())

    return {"nome": "Análise 5401", "message": "Arquivo processado com sucesso"}


def get_cotas(ativo , df_cotas):
    try:
        return df_cotas[df_cotas['Ativo'] == ativo].to_dict('records')[0]['Valor']
    except:
        return 0
@shared_task
def SincronizarCotasO2(data):
    try:
        data_datetime = datetime.strptime(data, "%Y-%m-%d")
        api = o2Api(os.environ.get("INTACTUS_LOGIN"), os.environ.get("INTACTUS_PASSWORD"))
        extratorCotas = ExtratorCotas(data_datetime)
        df_cotas = extratorCotas.df_cotas()

        df_ativos = api.get_ativos()

        df_ativos['data'] = data
        df_ativos['cota'] = df_ativos['cd_jcot'].apply(lambda x: get_cotas( x , df_cotas )   )

        cotas_a_importar = df_ativos[df_ativos['cota'] != 0 ]

        api.valor_cota_adicionar(cotas_a_importar)
        return {"nome": "Sincronização Cotas o2", "message": f"Cotas do dia {data} sincronizadas com suceso no o2"}
    except Exception as e:
        return {"nome": "Sincronização Cotas o2", "message": f"Erro de sincronização -> {e}"}
