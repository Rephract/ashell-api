# Generated by Django 4.0.2 on 2022-05-16 10:30

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('level', models.CharField(choices=[('debug', 'DEBUG'), ('info', 'INFO'), ('error', 'ERROR'), ('warning', 'WARNING')], max_length=20)),
                ('message_type', models.CharField(choices=[('log', 'LOG'), ('debug', 'DEBUG')], default='log', max_length=20)),
                ('message', models.TextField(max_length=1000)),
                ('code', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]
