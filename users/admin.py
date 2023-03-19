from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Division, DivisionMember


class DivisionMemberInline(admin.TabularInline):
    model = DivisionMember
    extra = 2  # how many rows to show


class DivisionAdmin(admin.ModelAdmin):
    inlines = (DivisionMemberInline,)
    list_display = (
        'name', 'description', 'is_active',
    )


admin.site.register(get_user_model())
admin.site.register(DivisionMember)
admin.site.register(Division, DivisionAdmin)
