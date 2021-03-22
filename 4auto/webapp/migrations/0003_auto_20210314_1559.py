# Generated by Django 3.1.7 on 2021-03-14 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20210314_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='items_photo', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='item',
            name='updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
