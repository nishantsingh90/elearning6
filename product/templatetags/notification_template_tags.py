from django import template
from notify.models import Notification,NotificationQueryset
from django.db.models import Count

register = template.Library()


@register.filter
def notification_count(user):
    if user.is_authenticated:
    
        qs = Notification.objects.filter(read=False,recipient=user).annotate(num_verb=Count('verb'))

        if qs.exists():
            return qs[0].num_verb
        
    return 0