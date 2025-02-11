# Generated by Django 5.1.5 on 2025-02-05 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_remove_pembayaran_jatuh_tempo_berikutnya_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaksi',
            name='tanggal_pembayaran',
            field=models.DateField(default='2025-01-01', verbose_name='Tanggal Pembayaran'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pembayaran',
            name='jatuh_tempo',
            field=models.DateField(blank=True, null=True, verbose_name='Jatuh Tempo Berikutnya'),
        ),
    ]
