# Generated by Django 4.1.9 on 2023-10-11 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='env',
            name='zone_name',
            field=models.CharField(default=None, max_length=20, null=True),
        ),
    ]