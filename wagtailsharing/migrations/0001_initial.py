# -*- coding: utf-8 -*-

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0030_index_on_pagerevision_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='SharingSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.CharField(max_length=255, db_index=True)),
                ('port', models.IntegerField(default=80)),
                ('site', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sharing_site', to='wagtailcore.Site')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='sharingsite',
            unique_together=set([('hostname', 'port')]),
        ),
    ]
