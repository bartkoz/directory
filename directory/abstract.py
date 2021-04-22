from django.db import models
from django.utils.translation import gettext_lazy as _


class TimestampAbstractModel(models.Model):
    """
    Holds created_at and updated_at fields which may turn
    out useful for every model someday.
    """

    created_at = models.DateTimeField(_("date created"), blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(_("date updated"), blank=True, auto_now=True)

    class Meta:
        abstract = True
