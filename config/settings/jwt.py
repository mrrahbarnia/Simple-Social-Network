from datetime import timedelta

from config.env import env

# For more settings
# Read everything from here - https://styria-digital.github.io/django-rest-framework-jwt/#additional-settings


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10)
}
