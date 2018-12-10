from django import template

register = template.Library()

@register.inclusion_tag('ces_admin/ces-dashboard.html', takes_context=True)
def assign_sms_variables(context):
    sms_context = {
        'open_sessions':  context['sms_open_sessions'],
        'canceled_sessions': context['sms_canceled_sessions'],
        # 'percentage_canceled': context['sms_percentage_canceled'],
    }

    return {'open_sessions': 1234}
