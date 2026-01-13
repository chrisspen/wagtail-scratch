from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from wagtail.rich_text import expand_db_html, RichText
from bs4 import BeautifulSoup

register = template.Library()

@register.filter
def richtext(value):
    if isinstance(value, RichText):
        html = str(value)
    elif value is None:
        html = ""
    else:
        html = expand_db_html(str(value))

    if getattr(settings, 'HIDE_SPANS', False):
        soup = BeautifulSoup(html, 'html.parser')
        for span in soup.find_all('span'):
            span.unwrap()  # Removes tag but keeps contents
        html = str(soup)

    return mark_safe(f'<div class="rich-text">{html}</div>')

@register.filter
def remove_highlight(value):
    """
    Strips <mark> tags from the content when settings.IS_READONLY is True,
    preserving the text inside. Otherwise passes the content through unchanged.
    """
    if getattr(settings, "IS_READONLY", False):
        value = re.sub(r"<mark[^>]*>", "", value)
        value = re.sub(r"</mark>", "", value)
    return value
