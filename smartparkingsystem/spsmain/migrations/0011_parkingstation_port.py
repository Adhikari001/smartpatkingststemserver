# Generated by Django 3.1 on 2020-10-18 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spsmain', '0010_auto_20201002_0844'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkingstation',
            name='port',
            field=models.IntegerField(null=True),
        ),
    ]