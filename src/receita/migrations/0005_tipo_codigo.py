# Generated by Django 4.2.16 on 2024-09-07 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receita', '0004_rename_preco_venda_valor'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipo',
            name='codigo',
            field=models.CharField(default='receita_tipo', max_length=100, unique=True),
            preserve_default=False,
        ),
    ]
