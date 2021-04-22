from django.db import models
from django.utils.translation import gettext_lazy as _


class TimestampAbstractModel(models.Model):
    created_at = models.DateTimeField(_("date created"), blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(_("date updated"), blank=True, auto_now=True)

    class Meta:
        abstract = True


class Subject(TimestampAbstractModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Teacher(TimestampAbstractModel):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(default="app/templates/misc/default_profile_picture.png")
    # this one is odd, it could be moved to nosql for example in real
    # conditions so it's not stored pointlessly here
    profile_picture_name = models.CharField(max_length=50, blank=True, null=True)
    email_address = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    room_number = models.CharField(max_length=10, blank=True, null=True)
    subjects_taught = models.ManyToManyField(Subject, blank=True, null=True)

    @property
    def taught_subjects_count(self):
        return self.subjects_taught.count()

    def __str__(self):
        return self.email_address
