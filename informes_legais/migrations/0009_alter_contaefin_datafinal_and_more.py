# Generated by Django 4.1.7 on 2024-04-01 13:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('informes_legais', '0008_alter_contaefin_datafinal_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contaefin',
            name='datafinal',
            field=models.DateTimeField(default=datetime.datetime(2099, 12, 31, 0, 0)),
        ),
        migrations.AlterField(
            model_name='movimentodetalhado',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2099, 12, 31, 0, 0)),
        ),
    ]
