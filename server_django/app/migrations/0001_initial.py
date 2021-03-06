# Generated by Django 2.2.1 on 2019-05-31 11:22

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('date_published', models.DateField(default=datetime.date.today)),
                ('date_added', models.DateField(default=datetime.date.today)),
                ('mgenre', models.CharField(choices=[('Action', 'Action'), ('Adventure', 'Adventure'), ('Drama', 'Drama'), ('Comedy', 'Comedy'), ('SyFy', 'SyFy')], default='Action', max_length=20)),
                ('mtype', models.CharField(choices=[('Movie', 'Movie'), ('Book', 'Book'), ('Series', 'Series')], default='Movie', max_length=20)),
                ('description', models.CharField(max_length=5000)),
                ('img', models.ImageField(default='gallery/no-img.png', upload_to='gallery')),
            ],
        ),
        migrations.CreateModel(
            name='MediaAuthor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('surname', models.CharField(max_length=70)),
                ('img', models.ImageField(default='gallery/no-img.png', upload_to='gallery')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(default='gallery/no-img.png', upload_to='gallery')),
                ('authentication', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TokenManagement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=1000)),
                ('date_added', models.DateField(default=datetime.datetime.today)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.User')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveIntegerField(default=0)),
                ('review', models.CharField(max_length=1000)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.User')),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Media')),
            ],
        ),
        migrations.AddField(
            model_name='media',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.MediaAuthor'),
        ),
    ]
