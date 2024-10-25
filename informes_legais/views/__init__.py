from django.http import HttpResponse , request



def start_view(request):
    return HttpResponse("Welcome to the API")