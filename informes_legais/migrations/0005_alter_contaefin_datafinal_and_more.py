# Generated by Django 4.1.7 on 2024-03-28 23:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('informes_legais', '0004_alter_contaefin_datafinal_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contaefin',
            name='datafinal',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 28, 20, 38, 49, 998164)),
        ),
        migrations.AlterField(
            model_name='movimentodetalhado',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 28, 20, 38, 50, 165)),
        ),
    ]
