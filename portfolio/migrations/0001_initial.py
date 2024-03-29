# Generated by Django 3.2.12 on 2022-04-07 16:41

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0066_collection_management_permissions'),
        ('wagtailimages', '0023_add_choose_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='PortfolioCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'portfolio categories',
            },
        ),
        migrations.CreateModel(
            name='PortfolioListingPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('custom_title', models.CharField(default='Title', help_text='Overwrites the default title', max_length=100)),
                ('subtitle', models.CharField(blank=True, default='Subtitle', help_text='Subtitle for the Portfolio Listing Page', max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='PortfolioDetailPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('subtitle', models.TextField(default='Subtitle', help_text='Overwrites the default title', max_length=300)),
                ('live_url', models.CharField(blank=True, max_length=100, null=True)),
                ('repo_url', models.CharField(blank=True, max_length=100, null=True)),
                ('text', wagtail.core.fields.StreamField([('title_and_text', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(blank=True, null=True, required=False)), ('text', wagtail.core.blocks.CharBlock(blank=True, null=True, required=False))]))], blank=True, null=True)),
                ('body', wagtail.core.fields.StreamField([('images', wagtail.images.blocks.ImageChooserBlock(template='streams/carousel.html'))], blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('categories', modelcluster.fields.ParentalManyToManyField(blank=True, to='portfolio.PortfolioCategory')),
                ('featured_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
