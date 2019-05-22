# Generated by Django 2.2.1 on 2019-05-15 11:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone
import generic_helpers.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Claimer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created at')),
                ('added_by', models.ForeignKey(blank=True, help_text='a user who created the entry', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'claimer',
                'verbose_name_plural': 'claimers',
            },
        ),
        migrations.CreateModel(
            name='EntryBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, blank=True, null=True)),
                ('reason', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created at')),
                ('country_code', models.TextField(blank=True, help_text='List of countries in alpha-2 format, one per line', null=True)),
                ('added_by', models.ForeignKey(blank=True, help_text='a user who created the entry', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('claimer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='django_fahrenheit.Claimer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='URL',
            fields=[
                ('entrybase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_fahrenheit.EntryBase')),
                ('pattern', models.CharField(max_length=512, unique=True)),
            ],
            options={
                'verbose_name': 'forbidden URL',
                'verbose_name_plural': 'forbidden URLs',
            },
            bases=('django_fahrenheit.entrybase',),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('body', models.TextField(blank=True, null=True)),
                ('attachment', models.FileField(blank=True, null=True, upload_to='')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created at')),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_fahrenheit.EntryBase')),
            ],
            options={
                'verbose_name': 'document',
                'verbose_name_plural': 'documents',
            },
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('entrybase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_fahrenheit.EntryBase')),
                ('object_id', models.IntegerField(verbose_name='object ID')),
                ('content_type', models.ForeignKey(limit_choices_to=generic_helpers.fields.AllowedContentTypes(generic_helpers.fields.GenericRelationField(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')), on_delete=django.db.models.deletion.CASCADE, related_name='ct_set_for_object', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'forbidden arbitrary object',
                'verbose_name_plural': 'forbidden arbitrary objects',
            },
            bases=('django_fahrenheit.entrybase',),
            managers=[
                ('gr', django.db.models.manager.Manager()),
            ],
        ),
    ]