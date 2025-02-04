# Generated by Django 5.1.5 on 2025-01-23 19:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tipekamar',
            name='gambar',
        ),
        migrations.CreateModel(
            name='KamarImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='kamar/')),
                ('tipe_kamar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='main.tipekamar')),
            ],
        ),
    ]
