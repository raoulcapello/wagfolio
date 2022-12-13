from django import forms
from django.db import models
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

from streams import blocks


class PortfolioListingPage(Page):
    "Lists all Portfolio Detail pages."
    parent_page_types = ["home.LandingPage"]

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        default="Title",
        help_text="Overwrites the default title",
    )
    subtitle = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="Subtitle",
        help_text="Subtitle for the Portfolio Listing Page",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("subtitle"),
            ]
        )
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["portfolio_items"] = PortfolioDetailPage.objects.live().public().order_by("-date")
        context["categories"] = PortfolioCategory.objects.all()

        return context


class PortfolioDetailPage(Page):
    """Portfolio Detail page."""

    parent_page_types = ["portfolio.PortfolioListingPage"]

    subtitle = models.TextField(
        max_length=300,
        blank=False,
        null=False,
        default="Subtitle",
        help_text="Overwrites the default title",
    )
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    live_url = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    live_url_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    live_url_popup = models.BooleanField(default=False)
    live_url_popup_text = models.TextField(max_length=250, blank=True, null=True, default="")
    repo_url = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    repo_url_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    text = StreamField(
        [
            ("title_and_text", blocks.TitleAndText()),
        ],
        blank=True,
        null=True,
    )
    body = StreamField(
        [
            (
                "images",
                ImageChooserBlock(
                    template="streams/carousel.html",
                ),
            ),
        ],
        blank=True,
        null=True,
    )
    date = models.DateField(blank=True, null=True)
    categories = ParentalManyToManyField("portfolio.PortfolioCategory", blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("subtitle"),
                FieldPanel("date"),
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
            ],
            heading="Details",
        ),
    ]

    details_panels = [
        MultiFieldPanel(
            [
                FieldPanel("live_url"),
                FieldPanel("live_url_name"),
                FieldPanel("live_url_popup"),
                FieldPanel("live_url_popup_text"),
            ],
            heading="Live URL",
        ),
        MultiFieldPanel(
            [
                FieldPanel("repo_url"),
                FieldPanel("repo_url_name"),
            ],
            heading="Repo URL",
        ),
    ]

    text_panels = [
        StreamFieldPanel("text"),
    ]

    image_panels = [
        ImageChooserPanel("featured_image"),
        StreamFieldPanel("body"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Page"),
            ObjectList(details_panels, heading="Details"),
            ObjectList(text_panels, heading="Content"),
            ObjectList(image_panels, heading="Images"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(Page.settings_panels, heading="Settings"),
        ]
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        portfolio_items = (
            PortfolioDetailPage.objects.live().public().order_by("-date").exclude(id=self.id)
        )
        context["portfolio_items"] = portfolio_items

        return context


@register_snippet
class PortfolioCategory(models.Model):
    name = models.CharField(max_length=100)

    panels = [
        FieldPanel("name"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "portfolio categories"
