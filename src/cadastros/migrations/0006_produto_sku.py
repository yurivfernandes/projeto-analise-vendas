# Generated by Django 3.2 on 2024-09-01 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0005_auto_20240901_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='sku',
            field=models.CharField(default=1111, max_length=16),
            preserve_default=False,
        ),
    ]