# Generated by Django 2.0.7 on 2018-07-08 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='sizes',
            field=models.CharField(choices=[('thirty', '30cm'), ('fifty', '50cm')], default='thirty', max_length=5, unique=True),
        ),
    ]