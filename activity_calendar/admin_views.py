from django.contrib import admin
from django.contrib.admin.utils import unquote
from django.conf.urls import url
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.text import capfirst
from django.utils.translation import gettext as _

from .models import Activity, CompoundActivity

class CustomAdminSite(admin.AdminSite):
    pass

class ActivityAdmin(admin.ModelAdmin):
    change_form_template = 'activity_calendar/admin/activity_change.html'
    activity_exception_template = 'activity_calendar/admin/activity_exceptions.html'

    def get_urls(self):
        urls = super(ActivityAdmin, self).get_urls()
        custom_urls = [
            path('activity_calendar/activity/<path:object_id>/exceptions/', self.admin_site.admin_view(self.activity_exception_view), name="activity_exceptions"),
        ]
        return custom_urls + urls

    def view_on_site(self, obj):
        # Only activities with an absolute url can be viewed on the site
        return obj.get_absolute_url()
    
    def activity_exception_view(self, request, object_id, extra_context=None):
        "The admin view that lists exceptions for an activity."

        # First check if the user can see this history.
        model = self.model
        obj = self.get_object(request, unquote(object_id))
        if obj is None:
            return self._get_obj_does_not_exist_redirect(request, model._meta, object_id)

        if not self.has_view_or_change_permission(request, obj):
            raise PermissionDenied

        opts = self.model._meta

        context = {
            **self.admin_site.each_context(request),
            'title': _('Exception Occurences: %s') % obj,
            'module_name': str(capfirst(opts.verbose_name_plural)),
            'object': obj,
            'opts': opts,
            'preserved_filters': self.get_preserved_filters(request),
            **(extra_context or {}),
        }

        request.current_app = self.admin_site.name

        return TemplateResponse(request, self.activity_exception_template, context)

admin_site = CustomAdminSite(name='admin_site')
admin_site.register(Activity, ActivityAdmin)
admin_site.register(CompoundActivity)
