# Generated by Django 3.2.13 on 2023-03-03 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Note',
                'verbose_name_plural': 'Notes',
            },
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=120, verbose_name='Text')),
                ('done', models.BooleanField(default=False, verbose_name='Done')),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.note', verbose_name='Note')),
            ],
            options={
                'verbose_name': 'Todo',
                'verbose_name_plural': 'Todos',
            },
        ),
    ]