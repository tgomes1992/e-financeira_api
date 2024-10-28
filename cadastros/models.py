from django.db import models

class Administrador(models.Model):
    cnpj = models.CharField(max_length=14, primary_key=True)
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class Fundos(models.Model):
    codigo = models.CharField(max_length=14, primary_key=True)
    nome = models.CharField(max_length=200)
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE, related_name="fundos")
    cnpj = models.CharField(max_length=14)


    def __str__(self):
        return self.nome
