# Generated by Django 3.2 on 2024-09-03 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0007_alter_produto_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendedor',
            name='codigo',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
