from django import template

register = template.Library()

@register.filter
def sizify(value):
    if value < 512000:
        value = value / 1024.0
        ext = "KB"
    
    elif value < 4194304000:
        value = value / 1048576.0
        ext = "MB"

    else:
        value = value / 107341824.0
        ext = "MB"
    return '%s %s' %(str(round(value, 2)), ext)


@register.filter
def sort_alphabetically(queryset):
    return sorted(queryset, key=lambda item: item.level.name)

