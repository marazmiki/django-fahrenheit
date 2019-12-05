from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models
from .settings import enable_added_by

ADDED_BY = ['added_by'] if enable_added_by() else []


class AddedByMixin:
    list_select_related = True

    def get_autocomplete_fields(self, request):
        return tuple(super().get_autocomplete_fields(request))\
               + tuple(ADDED_BY)

    def get_list_display(self, request):
        return tuple(super().get_list_display(request)) + tuple(ADDED_BY)

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        if ADDED_BY and not initial.get('added_by'):
            initial['added_by'] = request.user
        return initial


class DocumentInline(admin.TabularInline):
    model = models.Document
    extra = 0


@admin.register(models.Claimer)
class ClaimerAdmin(
    AddedByMixin,
    admin.ModelAdmin
):
    list_display = ['name', 'created_at']


@admin.register(models.URL)
class URLAdmin(
    AddedByMixin,
    admin.ModelAdmin
):
    list_select_related = True
    inlines = [DocumentInline]
    list_display = ['pattern', 'created_at']


@admin.register(models.Object)
class ObjectAdmin(
    AddedByMixin,
    admin.ModelAdmin
):
    inlines = [DocumentInline]
    list_display = ['__str__', 'content_type', 'object_id', 'created_at']
    fieldsets = (
        (_('A target object'), {'fields': [('content_type', 'object_id')]}),
        (None, {'fields': ADDED_BY + ['claimer']}),
        (None, {'fields': ['title', 'reason', 'created_at']}),
        (_('Country wide filtering'), {'fields': ['country_code']}),
    )
