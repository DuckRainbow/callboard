# Generated by Django 4.2.2 on 2024-12-18 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callboard', '0002_ad_author_ad_description_ad_price_ad_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания объявления'),
        ),
    ]
