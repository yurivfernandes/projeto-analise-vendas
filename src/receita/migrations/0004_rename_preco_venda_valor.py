# Generated by Django 3.2 on 2024-09-03 00:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('receita', '0003_alter_venda_produto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='venda',
            old_name='preco',
            new_name='valor',
        ),
    ]
