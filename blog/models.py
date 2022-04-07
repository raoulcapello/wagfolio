from datetime import datetime

from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet


class BlogListingPage(Page):
    parent_page_types = ["home.LandingPage"]
    max_count = 1

    subtitle = models.TextField(
        blank=True,
        max_length=500,
    )

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        all_posts = self.get_children().live().public().order_by("-first_published_at")
        paginator = Paginator(all_posts, 3)
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)  # Return results for this page number
        except PageNotAnInteger:
            posts = paginator.page(1)  # Return first page of results
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)  # Return last page of results

        context["posts"] = posts
        context["categories"] = BlogCategory.objects.all()

        return context


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "BlogPage",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )


class BlogTagIndexPage(Page):
    parent_page_types = ["home.LandingPage"]
    max_count = 1

    template = "blog/blog_listing_page.html"

    def get_context(self, request, *args, **kwargs):

        # Filter by tag
        tag = request.GET.get("tag")
        posts = BlogPage.objects.live().public().order_by("-first_published_at")

        # Update template context
        context = super().get_context(request, *args, **kwargs)
        if tag:
            posts = posts.filter(tags__name=tag)
        context["posts"] = posts

        return context


class BlogPage(Page):
    parent_page_types = ["blog.BlogListingPage"]

    date = models.DateField("Post date", default=datetime.now)
    summary = models.TextField(
        blank=True,
        max_length=500,
    )
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField("blog.BlogCategory", blank=True)
    internal_page = models.ForeignKey(
        "wagtailcore.Page",
        blank=True,
        null=True,
        related_name="+",
        help_text="Select an internal Wagtail page",
        on_delete=models.SET_NULL,
    )
    external_url = models.URLField(blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        return None

    search_fields = Page.search_fields + [
        index.SearchField("summary"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("date"),
                FieldPanel("tags"),
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
            ],
            heading="Blog information",
        ),
        FieldPanel("summary"),
        FieldPanel("body"),
        PageChooserPanel("internal_page"),
        FieldPanel("external_url"),
        InlinePanel("gallery_images", label="Gallery Images"),
    ]


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ForeignKey("wagtailimages.Image", on_delete=models.CASCADE, related_name="+")
    caption = models.CharField(max_length=250, blank=True)

    panels = [
        ImageChooserPanel("image"),
        FieldPanel("caption"),
    ]


class Skill(Orderable):
    skill = models.CharField(max_length=100)

    panels = [
        FieldPanel("skill"),
    ]


@register_snippet
class SkillCategory(models.Model):
    name = models.CharField(max_length=100)
    css_class = models.CharField(max_length=100, default="ai-code")

    panels = [
        FieldPanel("name"),
        FieldPanel("css_class"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "skill categories"


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("name"),
        ImageChooserPanel("icon"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "blog categories"
