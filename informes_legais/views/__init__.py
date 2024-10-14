from .views import *
from .views_5401 import *
from .views_efinanceira import *
from .GeracaoEfin import *
from .SincronizarCotasO2 import SincronizarCotas
from django.http import HttpResponse ,  JsonResponse
from informes_legais.tasks import timeConsumingtask
from django_celery_results.models import TaskResult



def delete_all_tasks(request):

    all_tasks = TaskResult.objects.all()
    for task in all_tasks:
        task.delete()
    return JsonResponse({"message":  "Tasks Deletadas"})


def gerar_efin_async(request):


    # async_task('informes_legais.tasks.gerar_efinanceira')


    return JsonResponse({"message":  "Gerando Efinanceira"})





def background_tasks(request):
    result = timeConsumingtask.delay()

    return  JsonResponse({"message":  "enviado para processamento"})
