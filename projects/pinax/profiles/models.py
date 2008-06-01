from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _

from timezones import TIMEZONE_CHOICES

class Profile(models.Model):
    
    user = models.ForeignKey(User, unique=True, verbose_name=_('user'))
    name = models.CharField(_('name'), max_length=50, null=True, blank=True)
    about = models.TextField(_('about'), null=True, blank=True)
    location = models.CharField(_('location'), max_length=40, null=True, blank=True)
    website = models.URLField(_('website'), null=True, blank=True)
    blogrss = models.URLField(_('blog rss/atom'), null=True, blank=True)
    timezone = models.CharField(_('timezone'), max_length=100,
        choices=TIMEZONE_CHOICES, default=settings.TIME_ZONE)
    
    def __unicode__(self):
        return self.user.username
    
    class Admin:
        pass
    
    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')