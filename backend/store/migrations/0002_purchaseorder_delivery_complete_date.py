# Generated by Django 5.0.4 on 2024-04-30 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='delivery_complete_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
