from django.contrib import admin
from .models import Activity, ActivitySlot, Participant

from .admin_views import *

class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 0


class ActivitySlotAdmin(admin.ModelAdmin):
    def recurrence_id_with_day(self, obj):
        if obj.recurrence_id is not None:
            return obj.recurrence_id.strftime("%a, %d %b %Y, %H:%M")
        return None
    recurrence_id_with_day.admin_order_field = 'recurrence_id'
    recurrence_id_with_day.short_description = 'Activity Start Date'

    list_display = ('id', 'title', 'parent_activity', 'recurrence_id_with_day', 'owner')
    list_filter = ['parent_activity', 'recurrence_id']
    list_display_links = ('id', 'title')

    # Not supported yet
    exclude = ('start_date', 'end_date')

    inlines = [ParticipantInline]

admin.site.register(ActivitySlot, ActivitySlotAdmin)
