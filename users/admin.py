from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Division, DivisionMember
from .forms import GroupAdminForm


class DivisionMemberInline(admin.TabularInline):
    model = DivisionMember
    extra = 2  # how many rows to show


class DivisionAdmin(admin.ModelAdmin):
    inlines = (DivisionMemberInline,)
    list_display = (
        'name', 'description', 'is_active',
    )


# Create a new Group admin.
class GroupAdmin(admin.ModelAdmin):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']


# # Unregister the original Group admin.
# admin.site.unregister(Group)
# # Register the new Group ModelAdmin.
# admin.site.register(Group, GroupAdmin)


admin.site.register(get_user_model())
admin.site.register(DivisionMember)
admin.site.register(Division, DivisionAdmin)
