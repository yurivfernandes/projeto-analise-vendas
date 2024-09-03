# Generated by Django 3.2 on 2024-09-03 00:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0008_alter_vendedor_codigo'),
        ('receita', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Imposto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.DecimalField(decimal_places=2, max_digits=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('loja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receita_imposto_set', to='cadastros.loja')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receita_imposto_set', to='receita.impostotipo')),
            ],
            options={
                'verbose_name': 'Receita Imposto',
                'verbose_name_plural': 'Receita Impostos',
                'db_table': 'receita_imposto',
                'unique_together': {('loja', 'tipo')},
            },
        ),
    ]
