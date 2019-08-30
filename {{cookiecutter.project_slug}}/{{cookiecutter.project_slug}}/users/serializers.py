from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
import pytz

class UserCreateSerializer(UserCreateSerializer):
    """
    Overide djoser UserCreateSerializer so we can also include timezone, since we can not use REQUIRED_FIELDS, because timezone field is not a string
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["timezone"] = serializers.CharField(default="UTC")

    def validate_timezone(self, value):
        if value in pytz.all_timezones:
            return value
        # if you want to raise a error do self.fail()
        return "UTC"