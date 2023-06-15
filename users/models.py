import datetime
import hashlib

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from django.db import models
from core.models import CommonInfo

from .managers import UserManager


def profile_directory_path(instance, filename):
    """
    Profile Upload Directory
    :param instance: the profile instance
    :param filename: the current filename
    :return: a new path for the upload directory
    """

    new_filename = hashlib.md5(
        datetime.datetime.now().isoformat().encode("utf-8")
    ).hexdigest()
    return "profile_pictures/{0}.{1}".format(new_filename, filename.split(".")[-1])


class User(CommonInfo, AbstractBaseUser, PermissionsMixin):
    """
        overriding user model
    """

    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    email = models.EmailField(max_length=500, unique=True)
    is_staff = models.BooleanField(default=False)

    furigana_fname = models.CharField(max_length=100, default="", null=False, blank=True)
    furigana_lname = models.CharField(max_length=100, default="", null=False, blank=True)
    position = models.CharField(max_length=100, default="", null=False, blank=True)

    avatar_url = models.ImageField(upload_to=profile_directory_path, null=True, blank=True)

    date_joined = models.DateTimeField(null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("first_name", "last_name")

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.handle = self.trimmed_email

        if not self.date_joined:
            self.date_joined = self.created_at

        return super(User, self).save(*args, **kwargs)

    def get_short_name(self):
        return f"{self.first_name}"

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}".title()

    @property
    def display_name(self):
        if self.first_name and self.last_name:
            return self.fullname
        return f"{self.email}"

    @property
    def trimmed_email(self):
        return self.email.split("@")[0]


class GroupProfile(CommonInfo):
    """User Divisions, similar to group but is more concerned on actual groups rather than authorizations"""

    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta(CommonInfo.Meta):
        verbose_name = "Group Profile"
        verbose_name_plural = "Group Profiles"
