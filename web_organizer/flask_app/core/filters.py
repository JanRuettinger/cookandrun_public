from . import core

@core.app_template_filter('event_date')
def event_date(date, format='%b %d, %Y'):
    return date.strftime(format)
