import re

from rest_framework import serializers


def restrict_username(username):
    if re.match(r'philo\d{2}$', username):
        msg = (
            'Username cannot be of a <philo> + <num> pattern. '
            'Please try another one.'
        )
        raise serializers.ValidationError(msg)
