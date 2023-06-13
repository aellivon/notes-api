from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .models import GroupProfile
from .forms import GroupAdminForm


# Create a new Group admin.
class GroupAdmin(admin.ModelAdmin):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']


# # Unregister the original Group admin.
admin.site.unregister(Group)
# # Register the new Group ModelAdmin.
admin.site.register(Group, GroupAdmin)


admin.site.register(get_user_model())
admin.site.register(GroupProfile)
