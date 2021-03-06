import datetime

from django import template
from django.utils import timezone
from django.utils.formats import date_format

from activity_calendar.forms import RegisterForActivitySlotForm

register = template.Library()

@register.simple_tag(takes_context=True)
def sign_up_slot_form(context, slot):
    user = context['request'].user

    # There is no logged in user, so return nothing instead
    if not user.is_authenticated:
        return None

    form = RegisterForActivitySlotForm(
        activity = context['activity'],
        user = user,
        recurrence_id=context['recurrence_id'],
        slot = slot,
        initial = {
            'slot_id': slot.id,
            'sign_up': slot.get_subscribed_participants().filter(id=user.id).count() == 0
        }
    )
    return form


@register.simple_tag(takes_context=True)
def get_opening_time(context, filter=None):
    activity_moment = context['activity_moment']
    open_date = activity_moment.start_time - activity_moment.parent_activity.subscriptions_open
    if filter:
        return date_format(open_date, filter)

    return open_date


@register.simple_tag(takes_context=True)
def opens_in_future(context):
    """ Returns whether the opening time is in the future """
    activity_moment = context['activity_moment']
    open_date = activity_moment.start_time - activity_moment.parent_activity.subscriptions_open
    return timezone.now() < open_date


@register.inclusion_tag("activity_calendar/slot_blocks/register_button.html", takes_context=True)
def register_button(context, slot):
    user = context['request'].user

    # There is no logged in user, so return nothing instead
    if not user.is_authenticated:
        return None

    sign_up = not slot.participants.filter(id=user.id).exists()

    form = RegisterForActivitySlotForm(
        activity = context['activity'],
        user = user,
        recurrence_id=context['recurrence_id'],
        activity_moment=context['activity_moment'],
        initial = {
            'slot_id': slot.id,
            'sign_up': sign_up,
        }
    )
    return {
        'form': form,
        'sign_up': sign_up,
        'error_messages': context.get('error_messages', None),
    }


@register.simple_tag(takes_context=True)
def form_rejection_reason(context, form=None):
    """ Presents the reason the form rejected. Works specifically only for the forms used in activity sign-ups """
    if form is None:
        # Take the default form if none is provided
        form = context['form']

    error = form.get_base_validity_error()

    if error:
        # Get the error code and search it up in the error_messages table
        return context['error_messages'].get(error.code, f'Undefined error occured: {error.code}')

    return ''

