# Generated by Django 2.2.16 on 2021-01-06 15:40

from django.db import migrations, models
import django.db.models.deletion
import wagtailsharing.models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('wagtailsharing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShareableRoutablePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtailsharing.models.ShareableRoutablePageMixin, 'wagtailcore.page'),
        ),
    ]