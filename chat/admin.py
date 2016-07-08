from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from chat.models import Account
from chat.forms import UserCreationForm

from django.contrib.auth.admin import UserAdmin

class EmployeeAdmin(UserAdmin):
    add_form = UserCreationForm
    list_display = ("username",)
    ordering = ("username",)

    fieldsets = (
        (None, {'fields': ('username', 'password', 'role', 'block', 'apartment', 'is_staff')}),
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password', 'role', 'block', 'apartment')}
            ),
        )

    filter_horizontal = ()

admin.site.register(Account, EmployeeAdmin)


