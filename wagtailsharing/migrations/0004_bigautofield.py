# Generated by Django 4.1.7 on 2023-03-17 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailsharing', '0003_delete_shareableroutablepage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharingsite',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
