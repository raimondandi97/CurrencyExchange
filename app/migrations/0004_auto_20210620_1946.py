# Generated by Django 3.2.4 on 2021-06-20 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210620_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='abv',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='currency',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='currency',
            name='name',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='currency',
            name='symbol',
            field=models.CharField(default='', max_length=10),
        ),
    ]
