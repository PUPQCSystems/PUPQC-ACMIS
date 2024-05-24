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

@register.filter
def custom_camel_case(value):
    """
    Converts a string to custom camel case:
        - Capitalizes first letter of each word except those in the exclusion list.
        - Lowercases words in the exclusion list.
        - Maintains spaces between words.
    """
    words = value.split()
    exclusion_words = ["is", "or", "of", "the", "in", "and"]

    formatted_words = [
        word.lower() if word.lower() in exclusion_words else word.capitalize() 
        for word in words
    ]
    return " ".join(formatted_words)  # Join words with spaces

