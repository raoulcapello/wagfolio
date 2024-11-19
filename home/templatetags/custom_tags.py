from django import template
from wagtail.core.models import Site

from site_settings.models import GoogleAnalyticsSettings

register = template.Library()


@register.simple_tag(takes_context=True)
def get_google_analytics_settings(context):
    request = context["request"]
    site = Site.find_for_request(request)
    return GoogleAnalyticsSettings.for_site(site)
