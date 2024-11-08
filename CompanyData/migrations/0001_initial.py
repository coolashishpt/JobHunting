# Generated by Django 5.1.2 on 2024-11-07 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('career_page', models.CharField(max_length=500)),
                ('employee_strength', models.IntegerField()),
            ],
        ),
    ]
