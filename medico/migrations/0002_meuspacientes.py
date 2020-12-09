# Generated by Django 3.1.3 on 2020-12-09 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0007_auto_20201208_0053'),
        ('medico', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeusPacientes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='medico.medico')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='usuario.usuario')),
            ],
        ),
    ]