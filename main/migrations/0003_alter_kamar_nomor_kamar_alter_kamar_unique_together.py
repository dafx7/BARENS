# Generated by Django 5.1.5 on 2025-03-05 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_tipekamar_deskripsi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kamar',
            name='nomor_kamar',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterUniqueTogether(
            name='kamar',
            unique_together={('nomor_kamar', 'lantai')},
        ),
    ]
