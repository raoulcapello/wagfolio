from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.blocks import RichTextBlock
from wagtail.core.fields import StreamField


@register_setting
class SocialMediaSettings(BaseSetting):
    """Social Media settings for our custom website."""

    github = models.URLField(blank=True, null=True, help_text="GitHub URL")
    linkedin = models.URLField(blank=True, null=True, help_text="LinkedIn URL")

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("github"),
                FieldPanel("linkedin"),
            ],
            heading="Social Media Settings",
        )
    ]


@register_setting
class CompanyDetailsSettings(BaseSetting):
    """Company details shared across the site."""

    owner = models.CharField(max_length=100, blank=True, null=True, default="Company Name")
    status = models.TextField(max_length=255, blank=True, null=True, default="Company Description")
    address = StreamField(
        [
            (
                "address",
                RichTextBlock(
                    template="streams/rich_text_block.html",
                ),
            ),
        ],
        null=True,
        blank=True,
    )
    company_ids = StreamField(
        [
            (
                "company_ids",
                RichTextBlock(
                    template="streams/rich_text_block.html",
                ),
            ),
        ],
        null=True,
        blank=True,
    )
    enable_address = models.BooleanField(default=True)
    enable_company_ids = models.BooleanField(default=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("owner"),
                FieldPanel("status"),
                FieldPanel("enable_address"),
                FieldPanel("enable_company_ids"),
                StreamFieldPanel("address"),
                StreamFieldPanel("company_ids"),
            ],
            heading="Company Details",
        )
    ]
