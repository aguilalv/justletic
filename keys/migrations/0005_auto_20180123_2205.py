# Generated by Django 2.0.1 on 2018-01-23 22:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('keys', '0004_key_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='key',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='keys.User'),
        ),
    ]
