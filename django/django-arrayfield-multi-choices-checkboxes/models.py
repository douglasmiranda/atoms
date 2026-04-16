from django.db import models

from .fields import MultipleChoiceArrayField


class Config(models.Model):
    # https://docs.python.org/3/library/datetime.html#datetime.date.weekday
    class Weekdays(models.IntegerChoices):
        MONDAY = 0, "Monday"
        TUESDAY = 1, "Tuesday"
        WEDNESDAY = 2, "Wednesday"
        THURSDAY = 3, "Thursday"
        FRIDAY = 4, "Friday"
        SATURDAY = 5, "Saturday"
        SUNDAY = 6, "Sunday"

        @classmethod
        def get_default_weekdays(cls):
            return [
                cls.MONDAY,
                cls.TUESDAY,
                cls.WEDNESDAY,
                cls.THURSDAY,
                cls.FRIDAY,
            ]

    valid_weekdays = MultipleChoiceArrayField(
        models.PositiveSmallIntegerField("Valid week days", choices=Weekdays),
        size=7,
        default=Weekdays.get_default_weekdays,
    )
