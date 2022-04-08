from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting


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

    name = models.CharField(max_length=100, blank=True, null=True, default="Company Name")
    description = models.TextField(
        max_length=255, blank=True, null=True, default="Company Description"
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("description"),
            ],
            heading="Company Details",
        )
    ]
