# Generated by Django 3.1.3 on 2020-12-07 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('laboratorio', '0002_auto_20201203_0425'),
        ('usuario', '0005_exames'),
    ]

    operations = [
        migrations.AddField(
            model_name='exames',
            name='laboratorio',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='laboratorio.laboratorio'),
        ),
        migrations.DeleteModel(
            name='Exame',
        ),
    ]
