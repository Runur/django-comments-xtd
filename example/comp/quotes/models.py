from __future__ import unicode_literals

from datetime import datetime

import django
from django.db import models
from django.db.models import permalink
from django.utils.encoding import python_2_unicode_compatible


class PublicManager(models.Manager):
    """Returns published quotes that are not in the future."""
    
    def published(self):
        return self.get_queryset().filter(publish__lte=datetime.now())


@python_2_unicode_compatible
class Quote(models.Model):
    """Quote, that accepts comments."""

    title = models.CharField('title', max_length=200)
    slug = models.SlugField('slug', unique_for_date='publish')
    quote = models.TextField('quote')
    author = models.CharField('author', max_length=255)
    url_source = models.URLField('url source', blank=True, null=True)    
    allow_comments = models.BooleanField('allow comments', default=True)
    publish = models.DateTimeField('publish', default=datetime.now)

    objects = PublicManager()

    class Meta:
        db_table = 'comp_quotes'
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ('quotes-quote-detail', (), {'slug': self.slug})
