# Generated by Django 3.2.9 on 2022-04-13 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cornix', '0007_myclient_investment_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='next_step',
            field=models.CharField(max_length=255),
        ),
    ]
