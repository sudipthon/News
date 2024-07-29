# Generated by Django 5.0.2 on 2024-07-01 08:21

import baseapp.models
import ckeditor_uploader.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Popup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='popup/')),
                ('link', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url_name', models.CharField(blank=True, max_length=100, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='baseapp.category')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('party_name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('posted_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=baseapp.models.get_upload_path)),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('section', models.CharField(choices=[('side', 'Side'), ('main', 'Main')], default='main', max_length=100)),
                ('categories', models.ManyToManyField(blank=True, related_name='category_ads', to='baseapp.category')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.TextField()),
                ('featured_image', models.ImageField(blank=True, default='None', null=True, upload_to=baseapp.models.get_upload_path)),
                ('first_paragraph', models.TextField(blank=True, null=True)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('posted_on', models.DateTimeField(blank=True, null=True)),
                ('posted_on_bs', models.CharField(blank=True, max_length=100, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('views_count', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('Published', 'Published'), ('Draft', 'Draft'), ('Deleted', 'Deleted')], default='Draft', max_length=100)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_posts', to=settings.AUTH_USER_MODEL)),
                ('categories', models.ManyToManyField(related_name='category_posts', to='baseapp.category')),
                ('tags', models.ManyToManyField(related_name='tag_posts', to='baseapp.tags')),
            ],
            options={
                'ordering': ['-posted_on'],
            },
        ),
    ]
