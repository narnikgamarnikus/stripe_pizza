# Generated by Django 2.0.7 on 2018-07-10 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzas', '0006_auto_20180709_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='SKU_id',
            field=models.CharField(max_length=25, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='size',
            field=models.CharField(choices=[('thirty', '30cm'), ('fifty', '50cm')], max_length=6),
        ),
    ]
