# Generated by Django 5.1.2 on 2024-11-07 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CompanyData', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyname',
            name='employee_strength',
            field=models.CharField(max_length=100),
        ),
    ]