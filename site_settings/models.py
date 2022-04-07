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
