from django.views import View
from django.http import HttpResponse , JsonResponse
import boto3
import zipfile
from io import BytesIO


class S3ManagementClient():

    def __init__(self):
        self.client = boto3.client('s3')
        self.bucket = "s3://projetos-desenvolvidos-por-escrituracao/"
        self.bucket_name = self.bucket.replace('s3://', '').split('/')[0]


    def upload_unique(self , key , body):
        self.client.put_object(Bucket=self.bucket_name, Key=key, Body=body)


    def create_and_upload(self , prefix):
        '''método para criar um arquivo zipado através da pasta'''
        objects = self.client.list_objects_v2(Bucket=self.bucket_name)
        file_keys = [file['Key'] for file in objects['Contents'] if prefix in file['Key']]
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for file_key in file_keys:
                arquivo = self.client.get_object(Bucket=self.bucket_name, Key=file_key)
                zip_file.writestr(file_key[len(prefix):], arquivo['Body'].read())

        zip_buffer.seek(0)  # Reset buffer position before uploading
        self.client.put_object(Bucket=self.bucket_name, Key=f'zip_bucket.zip', Body=zip_buffer)


        #continuação que realiza o donwload do arquivo zipado

        response = self.client.get_object(Bucket=self.bucket_name, Key=f'zip_bucket.zip')
        zip_content = response['Body'].read()

        # Set the content type for the HTTP response
        response = HttpResponse(zip_content, content_type='application/zip')

        # Set the content disposition to force download
        response['Content-Disposition'] = f'attachment; filename="zip_bucket.zip"'

        return response

    def delete_all(self ,prefix=""):
        response = self.client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
        # Extract object keys
        objects_to_delete = [{'Key': obj['Key']} for obj in response.get('Contents', [])]
        # Delete objects
        if objects_to_delete:
            self.client.delete_objects(Bucket=self.bucket_name, Delete={'Objects': objects_to_delete})
            return JsonResponse({"message": "Arquivos deletados"})
        else:
            return JsonResponse({"message": "Sem arquivos para remover"})

    def delete_containing(self, text):
        response = self.client.list_objects_v2(Bucket=self.bucket_name)
        # Extract object keys
        objects_to_delete_pre = [{'Key': obj['Key']} for obj in response.get('Contents', [])]
        # Delete objects
        objects_to_delete = [item for item in objects_to_delete_pre if item['Keys'].contains(text)]

        if objects_to_delete:
            self.client.delete_objects(Bucket=self.bucket_name, Delete={'Objects': objects_to_delete})
            return JsonResponse({"message": "Arquivos deletados"})
        else:
            return JsonResponse({"message": "Sem arquivos para remover"})

    def delete_by_key(self, key):
        response = self.client.list_objects_v2(Bucket=self.bucket_name)
        # Extract object keys
        objects_to_delete = [{'Key': key}]

        if objects_to_delete:
            self.client.delete_objects(Bucket=self.bucket_name, Delete={'Objects': objects_to_delete})
            return JsonResponse({"message": "Arquivos deletados"})
        else:
            return JsonResponse({"message": "Sem arquivos para remover"})


    def list_bucket_files(self):
        objects = self.client.list_objects_v2(Bucket=self.bucket_name)
        try:
            file_keys = [file['Key'] for file in objects['Contents']]
            return file_keys
        except:
            return []

    def list_bucket_files_filtered(self,filter):
        objects = self.client.list_objects_v2(Bucket=self.bucket_name)
        file_keys = [file['Key'] for file in objects['Contents'] if filter in file['Key']]
        return file_keys

    def download_by_key(self,key):
        response = self.client.get_object(Bucket=self.bucket_name, Key=key)
        file_content = response['Body'].read()
        response = self.client.head_object(Bucket=self.bucket_name, Key=key)
        response = HttpResponse(file_content, content_type=response['ContentType'])
        response['Content-Disposition'] = f'attachment; filename="{key}"'
        return response


