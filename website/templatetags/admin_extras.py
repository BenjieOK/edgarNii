from django import template
from django.utils import timezone

from website.models import BlogPost, ContactMessage, Event

register = template.Library()


@register.simple_tag
def unread_message_count():
    return ContactMessage.objects.filter(is_read=False).count()


@register.simple_tag
def upcoming_event_count():
    return Event.objects.filter(date_time__gte=timezone.now()).count()


@register.simple_tag
def published_post_count():
    return BlogPost.objects.filter(is_published=True).count()
