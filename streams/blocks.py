from django import forms
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock

# from portfolio.models import PortfolioDetailPage


class Button(blocks.StructBlock):

    text = blocks.CharBlock(
        max_length=50,
        help_text="Button text",
    )
    disabled = blocks.BooleanBlock(
        help_text="Show button as disabled",
        required=False,
        default=False,
    )

    class Meta:
        icon = "tick-inverse"
        label = "Default Button"
        template = "streams/default_button.html"


class JumpToButton(Button):
    section_id = blocks.CharBlock(
        max_length=50,
        help_text="Jump to section, i.e. 'about' jumps to #about on the same page",
    )

    class Meta:
        icon = "tick-inverse"
        label = "Jump-To-Section Button"


class ButtonGroup(blocks.StructBlock):

    buttons = blocks.ListBlock(
        JumpToButton(),
    )

    class Meta:
        template = "streams/button_block.html"
        icon = "tick"
        label = "Default Button Group"


class DownloadButton(Button):

    icon = blocks.CharBlock(
        max_length=50,
        help_text="Set a CSS class for the button icon",
        default="ai-arrow-down-circle mt-n1 me-2",
    )
    document = DocumentChooserBlock(required=False)

    # TODO: Add link to Wagtail Documents

    class Meta:
        icon = "download"
        label = "Download Button"
        template = "streams/download_button.html"


class DownloadButtonList(blocks.StructBlock):

    buttons = blocks.ListBlock(
        DownloadButton(),
    )

    class Meta:
        template = "streams/icon_button_block.html"
        icon = "download"
        label = "Download Button Group"


class LinkValue(blocks.StructValue):
    """Additional logic for links"""

    def url(self) -> str:
        internal_page = self.get("internal_page")
        external_link = self.get("external_link")
        if internal_page:
            return internal_page.url
        elif external_link:
            return external_link
        return ""


class Link(blocks.StructBlock):

    link_text = blocks.CharBlock(
        max_length=50,
        default="More Detail",
    )
    internal_page = blocks.PageChooserBlock(
        required=False,
    )
    external_link = blocks.URLBlock(
        required=False,
    )

    class Meta:
        value_class = LinkValue

    def clean(self, value):
        internal_page = value.get("internal_page")
        external_link = value.get("external_link")
        errors = {}
        if internal_page and external_link:
            errors["internal_page"] = ErrorList(
                ["Both of these fields cannot be filled. Please select or enter only one option."]
            )
            errors["external_link"] = ErrorList(
                ["Both of these fields cannot be filled. Please select or enter only one option."]
            )
        elif not internal_page and not external_link:
            errors["internal_page"] = ErrorList([""])
            errors["external_link"] = ErrorList([""])

        if errors:
            raise ValidationError("VAlidation error in your link", params=errors)


class Card(blocks.StructBlock):

    title = blocks.CharBlock(
        max_length=100,
        help_text="Bold title text for this card. Max length of 100 characters",
    )
    text = blocks.TextBlock(
        max_length=255,
        help_text="Optional text for card. Max length 255",
    )
    image = ImageChooserBlock(
        help_text="Image will be automagically cropped",
        required=False,
    )
    link = Link(
        help_text="Enter a link or select a page",
    )


class CardList(blocks.StructBlock):

    cards = blocks.ListBlock(
        Card(),
    )

    class Meta:
        template = "streams/cards_block.html"
        icon = "image"
        label = "Standard Cards"


class SkillCard(blocks.StructBlock):
    skill = blocks.CharBlock(
        max_length=100,
        help_text="A personal skill to showcase on the page",
    )
    categories = SnippetChooserBlock("blog.SkillCategory", required=False)

    class Meta:
        label = "Skill Card"


class SkillCardList(blocks.StructBlock):

    skill_cards = blocks.ListBlock(
        SkillCard(),
    )

    class Meta:
        template = "streams/skill_cards_block.html"
        icon = "placeholder"
        label = "Skill Cards"


class USP(blocks.StructBlock):

    title = blocks.CharBlock(
        help_text="Choose a title",
    )
    description = blocks.TextBlock(
        help_text="Describe a Unique Selling Point",
        rows=2,
    )
    image = ImageChooserBlock(
        help_text="Select image",
    )

    class Meta:
        label = "USP"


class USPList(blocks.StructBlock):

    title = blocks.CharBlock(
        help_text="Add your Unique Selling Points",
        default="What I Do Best",
    )
    usps = blocks.ListBlock(
        USP(),
    )

    class Meta:
        template = "streams/usp_list_block.html"  # Default
        icon = "placeholder"
        label = "Unique Selling Points"


class Testimonial(blocks.StructBlock):
    text = blocks.TextBlock(
        help_text="Quote text",
    )
    author = blocks.CharBlock(help_text="Author of quote")

    class Meta:
        label = "Testimonial"
        template = "streams/testimonial.html"


class TestimonialList(blocks.StructBlock):

    testimonials = blocks.ListBlock(
        Testimonial(),
    )

    class Meta:
        label = "Testimonials"
        template = "streams/testimonial_block.html"


class RadioSelectBlock(blocks.ChoiceBlock):
    """Use a radio select choice widget."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field.widget = forms.RadioSelect(choices=self.field.widget.choices)


class Greeting(blocks.StructBlock):

    greeting = blocks.CharBlock(
        help_text="Big caption on top of landing page",
        label="Title",
        default="Hi! I'm Raoul",
    )
    lead_text = blocks.CharBlock(
        help_text="Subheading text under the banner title",
        label="Subtitle",
        default="Full Stack Python/Django/React Developer",
    )
    main_profile_picture = ImageChooserBlock(
        help_text="Big profile picture is big",
    )
    image_aligment = RadioSelectBlock(
        choices=(
            ("left", "Image to the left"),
            ("right", "Image to the right"),
        ),
        default="right",
        help_text="Configure image to be displayed on one side, text on the other.",
    )
    buttons = ButtonGroup()
    download_buttons = DownloadButtonList()

    class Meta:
        template = "streams/title_block.html"  # Default
        icon = "edit"  # Default
        label = "Hero Greeting Section"
        help_text = "Text field"


class Carousel(blocks.StructBlock):
    images = blocks.ListBlock(
        ImageChooserBlock(),
    )


class PortfolioCarousel(blocks.StructBlock):
    title = blocks.CharBlock(blank=True, null=True)

    class Meta:
        template = "streams/portfolio_carousel.html"

    # def get_context(self, request, *args, **kwargs):
    #     context = super().get_context(request, *args, **kwargs)
    #     context["portfolio_items"] = (
    #         PortfolioDetailPage.objects.live().public().all().order_by("-created")
    #     )

    #     return context


class PortfolioServices(blocks.StructBlock):
    """Services provided for a portfolio item."""

    services = blocks.ListBlock(
        blocks.CharBlock(),
    )


class PortfolioClient(blocks.StructBlock):
    """Client details of a portfolio item."""

    name = blocks.CharBlock(blank=True, null=True)
    services = PortfolioServices()
    website = blocks.CharBlock(blank=True, null=True)


class TitleAndText(blocks.StructBlock):
    title = blocks.CharBlock(required=False, blank=True, null=True)
    text = blocks.CharBlock(required=False, blank=True, null=True)

    class Meta:
        template = "streams/title_and_text.html"
