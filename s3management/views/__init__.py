from .s3control import S3ManagementClient
from django.http import HttpResponse , JsonResponse
from django.shortcuts import render


def list_bucket_files(request):
    s3 = S3ManagementClient()

    arquivos = s3.list_bucket_files()


    if request.method == 'POST':
        print (request.POST)

        arquivos = s3.list_bucket_files_filtered(request.POST['q'])


    return render(request, 's3management/s3files.html' , {'arquivos' : arquivos})


def dowload_prefix_as_zip(request):
    if request.method == 'POST':

        prefix = ""
        s3 = S3ManagementClient()
        return s3.create_and_upload(prefix)
    else:
        return render(request , 's3management/download_by_prefix.html')


def download_unique(request):
    s3 = S3ManagementClient()
    key = request.GET.get("key")
    return s3.download_by_key(key)


def delete_by_key(request):
    s3 = S3ManagementClient()
    key = request.GET.get('key')
    return s3.delete_by_key(key)




def clear_folder(request, folder):
    s3 = S3ManagementClient()
    return s3.delete_all(folder)