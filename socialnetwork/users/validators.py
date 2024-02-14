import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def number_validator(password):
    regex = re.compile('[0-9]')
    if regex.search(password) == None:
        raise ValidationError(
            _('Password must include numbers.'),
            code='password_must_include_numbers'
        )

def letter_validator(password):
    regex = re.compile('[a-zA-Z]')
    if regex.search(password) == None:
        raise ValidationError(
            _('Password must include letters.'),
            code='password_must_include_letters'
        )

def special_char_validator(password):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(password) == None:
        raise ValidationError(
            _('Password must include special character.'),
            code='password_must_include_special_char'
        )
