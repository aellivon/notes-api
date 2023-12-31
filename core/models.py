

from django.db import models


class ActiveManager(models.Manager):
    """
        This class defines a new default query set so the project can always
            filter data that is active
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class CommonInfo(models.Model):
    """
        This class is the parent class for all the models
    """

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # This allows us to escape to default django query set if
    #   later in the project I need it
    all_objects = models.Manager()

    # for active query set
    objects = ActiveManager()

    class Meta:
        abstract = True
