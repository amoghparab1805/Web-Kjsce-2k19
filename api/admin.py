from django.contrib import admin
from .models import *
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class UserAdmin(UserAdmin):
    form = UserChangeForm
    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                "fields": (
                    "uid",
                    "email",
                    "phone_number",
                    "first_name",
                    "last_name",
                    "provider_id",
                )
            },
        ),
    )

admin.site.register(User)
