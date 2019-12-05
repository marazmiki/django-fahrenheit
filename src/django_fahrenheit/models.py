from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from generic_helpers.fields import GenericRelationField

from .settings import enable_added_by


class AddedBy(models.Model):
    if enable_added_by():
        added_by = models.ForeignKey(
            to=settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            null=True,
            blank=True,
            help_text=_('a user who created the entry')
        )

    class Meta:
        abstract = True


class Claimer(AddedBy):
    name = models.CharField(
        max_length=255,
    )
    created_at = models.DateTimeField(
        verbose_name=_('created at'),
        default=now,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('claimer')
        verbose_name_plural = _('claimers')


class EntryBase(AddedBy):
    title = models.CharField(max_length=255, null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(
        verbose_name=_('created at'),
        default=now,
    )
    country_code = models.TextField(
        null=True,
        blank=True,
        help_text=_('List of countries in alpha-2 format, one per line')
    )
    claimer = models.ForeignKey(
        to='Claimer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title or ''

class Document(models.Model):
    entry = models.ForeignKey(
        to='EntryBase',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    body = models.TextField(
        null=True,
        blank=True
    )
    attachment = models.FileField(
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_('created at'),
        default=now,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('document')
        verbose_name_plural = _('documents')


class URL(EntryBase):
    pattern = models.CharField(
        max_length=512,
        unique=True
    )

    def __str__(self):
        return self.pattern

    class Meta:
        verbose_name = _('forbidden URL')
        verbose_name_plural = _('forbidden URLs')


class Object(EntryBase):
    content_object = GenericRelationField()

    class Meta:
        verbose_name = _('forbidden arbitrary object')
        verbose_name_plural = _('forbidden arbitrary objects')


