from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

#Black listed characters for validations
BLACKLIST = [';', "'", '"', '=', '(', ')', '<', '>', '--', '/*', '*/', '@', 
             'SELECT', '<script>', '</script>', 'script', 'insert', '$', '^',
             '!', '#', '%', '&', '*', '-', '+', '\\', '/', ':', ',', '?']

def program_name_validate(value):
    n = 0
    count = 0
    for char in value:
        if char in BLACKLIST[n]:
            count += 1  
        n += 1

    if count > 0:
        raise ValidationError(_("Sorry, the program name cannot contain any of the following characters: `!@#$%^&*()-+\"'/;:,<>?`"))

    else:
        return value

 
    
def abbreviation_validate(value):
    if value in BLACKLIST:
        raise ValidationError(_("Sorry, this characters is not valid. Please enter a valid characters"))

    else:
        return value


    

def description_validate(value):
    if value in BLACKLIST:
        raise ValidationError(_("Sorry, this characters is not valid. Please enter a valid characters"))

    else:
        return value

