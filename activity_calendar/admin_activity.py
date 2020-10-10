from django.contrib import admin
from django.contrib.admin.utils import unquote
from django.conf.urls import url
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.text import capfirst
from django.utils.translation import gettext as _

from .models import Activity, CompoundActivity

class ActivityAdmin(admin.ModelAdmin):
    change_form_template = 'activity_calendar/admin/activity_change.html'

    list_display = ('id', 'title', 'start_date', 'is_recurring', 'subscriptions_required', )
    list_filter = ['subscriptions_required']
    list_display_links = ('id', 'title')

    def is_recurring(self, obj):
        return obj.is_recurring        
    is_recurring.boolean = True

    def view_on_site(self, obj):
        # Only activities with an absolute url can be viewed on the site
        return obj.get_absolute_url()

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra = extra_context or {}
        extra['compound_opts'] = CompoundActivity._meta
        obj = self.get_object(request, unquote(object_id))
        if obj is not None:
            extra['compound'] = obj.compound
        return super().change_view(request, object_id, form_url, extra_context=extra)

class ActivityForCompoundAdmin(ActivityAdmin):
    def get_queryset(self, request):
        qs = super(ActivityForCompoundAdmin, self).get_queryset(request)

        # We only care about activities in our compoundActivity (which is encoded in the URL)
        return qs.filter(compound=request.resolver_match.kwargs['object_id'])

class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 0
    show_change_link = True

    fields = ('title', 'location', 'start_date', 'end_date')
    readonly_fields = fields

class CompoundActivityAdmin(admin.ModelAdmin):
    change_form_template = 'activity_calendar/admin/compound_activity_change.html'
    activity_exception_template = 'activity_calendar/admin/activity_exceptions.html'

    activity_for_compound_admin = None
    # inlines = [ActivityInline]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.activity_for_compound_admin = self.get_activity_for_compound_admin()

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # hide ActivityInline in the add view
            if not isinstance(inline, ActivityInline) or obj is not None:
                yield inline.get_formset(request, obj), inline

    def get_activity_for_compound_admin(self):
        return ActivityForCompoundAdmin(Activity, self.admin_site)

    def get_urls(self):
        urls = super(CompoundActivityAdmin, self).get_urls()
        custom_urls = [
            path('activity_calendar/compoundactivity/<path:object_id>/exceptions/', self.admin_site.admin_view(self.activity_exception_view), name="activity_exceptions"),
        ]
        return custom_urls + urls
    
    @admin.options.csrf_protect_m
    def activity_exception_view(self, request, object_id, extra_context=None):
        "The admin view that lists exceptions for an activity."

        # First check if the user can see these occurence exceptions.
        model = self.model
        obj = self.get_object(request, unquote(object_id))
        if obj is None:
            return self._get_obj_does_not_exist_redirect(request, model._meta, object_id)

        if not self.has_view_or_change_permission(request, obj):
            raise PermissionDenied

        opts = self.model._meta

        context = {
            **self.admin_site.each_context(request),
            'object': obj,
            'preserved_filters': self.get_preserved_filters(request),
            **self.activity_for_compound_admin.changelist_view(request, extra_context).context_data,
            'opts': opts,
            'title': _('Exception Occurences: %s') % obj,
            'module_name': str(capfirst(opts.verbose_name_plural)),
        }
        
        request.current_app = self.admin_site.name

        return TemplateResponse(request, self.activity_exception_template, context)

admin.site.register(Activity, ActivityAdmin)
admin.site.register(CompoundActivity, CompoundActivityAdmin)

