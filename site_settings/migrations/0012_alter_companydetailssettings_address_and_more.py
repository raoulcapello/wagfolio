# Generated by Django 4.1.4 on 2022-12-14 07:26

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("site_settings", "0011_auto_20220408_1543"),
    ]

    operations = [
        migrations.AlterField(
            model_name="companydetailssettings",
            name="address",
            field=wagtail.fields.StreamField(
                [
                    (
                        "address",
                        wagtail.blocks.RichTextBlock(
                            template="streams/rich_text_block.html"
                        ),
                    )
                ],
                blank=True,
                null=True,
                use_json_field=True,
            ),
        ),
        migrations.AlterField(
            model_name="companydetailssettings",
            name="company_ids",
            field=wagtail.fields.StreamField(
                [
                    (
                        "company_ids",
                        wagtail.blocks.RichTextBlock(
                            template="streams/rich_text_block.html"
                        ),
                    )
                ],
                blank=True,
                null=True,
                use_json_field=True,
            ),
        ),
    ]
