# Generated by Django 3.2.12 on 2022-04-08 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_rename_site_description_landingpage_company_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='landingpage',
            name='company_description',
            field=models.TextField(blank=True, default='Company Description', null=True),
        ),
    ]
