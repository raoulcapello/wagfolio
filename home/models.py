from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.core.fields import StreamBlock, StreamField
from wagtail.core.models import Orderable, Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock

from blog.models import SkillCategory
from portfolio.models import PortfolioCategory, PortfolioDetailPage
from streams import blocks


class HomePageCarouselImages(Orderable):
    """Between 1 and 5 images for the home page carousel."""

    page = ParentalKey("home.LandingPage", related_name="carousel_images")
    carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("carousel_image"),
    ]


class LandingPage(Page):
    parent_page_types = ["wagtailcore.Page"]
    # subpage_types = ["blog.BlogListingPage", "blog.BlogTagIndexPage"]
    max_count = 1

    greeting = models.CharField(
        max_length=100,
        blank=False,
        null=True,
    )
    lead_text = models.CharField(
        max_length=100,
        blank=False,
        null=True,
    )
    main_profile_picture = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    buttons = StreamField(
        [
            ("buttons", blocks.JumpToButton()),
        ],
        blank=True,
        null=True,
        use_json_field=True,
    )
    download_buttons = StreamField(
        [
            (
                "buttons",
                blocks.DownloadButton(),
            ),
        ],
        blank=True,
        null=True,
        use_json_field=True,
    )
    body = StreamField(
        [
            (
                "portfolio_carousel",
                blocks.PortfolioCarousel(),
            ),
            (
                "usps",
                blocks.USPList(),
            ),
            (
                "skill_cards",
                blocks.SkillCardList(),
            ),
            (
                "testimonials",
                blocks.TestimonialList(),
            ),
            (
                "testimonial",
                SnippetChooserBlock(
                    target_model="testimonials.Testimonial",
                    template="streams/testimonial.html",
                ),
            ),
        ],
        blank=True,
        null=True,
        use_json_field=True,
    )
    image_carousel_enabled = models.BooleanField(default=False)
    portfolio_carousel_enabled = models.BooleanField(default=False)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("greeting"),
                FieldPanel("lead_text"),
                FieldPanel("main_profile_picture"),
                FieldPanel("buttons"),
                FieldPanel("download_buttons"),
            ],
            heading="Hero Section",
        )
    ]

    body_panels = [
        FieldPanel("body"),
    ]

    image_carousel_panels = [
        MultiFieldPanel(
            [
                FieldPanel("portfolio_carousel_enabled", heading="Enable Portfolio Carousel"),
            ],
            heading="Portfolio Carousel",
        ),
        MultiFieldPanel(
            [
                FieldPanel("image_carousel_enabled", heading="Enable Image Carousel"),
                InlinePanel("carousel_images", max_num=5, min_num=0, label="Add image"),
            ],
            heading="Image Carousel",
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Header"),
            ObjectList(body_panels, heading="Body"),
            ObjectList(image_carousel_panels, heading="Carousel"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(Page.settings_panels, heading="Settings"),
        ]
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["skill_categories"] = SkillCategory.objects.all()
        context["categories"] = PortfolioCategory.objects.all()
        context["portfolio_items"] = PortfolioDetailPage.objects.live().public().order_by("-date")

        return context
