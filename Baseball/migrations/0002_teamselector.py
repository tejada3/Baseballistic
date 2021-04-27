# Generated by Django 3.2 on 2021-04-23 20:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Baseball', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamSelector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Baseball.teams')),
            ],
        ),
    ]
