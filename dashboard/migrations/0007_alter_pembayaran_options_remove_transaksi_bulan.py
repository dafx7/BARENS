# Generated by Django 5.1.5 on 2025-02-05 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_transaksi_tanggal_pembayaran_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pembayaran',
            options={},
        ),
        migrations.RemoveField(
            model_name='transaksi',
            name='bulan',
        ),
    ]
