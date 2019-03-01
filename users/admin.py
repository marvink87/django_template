from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form_template = 'admin/users/customuser/add_form.html'
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    ordering = ('-admin', '-staff', 'email', 'last_name', 'first_name')
    search_fields = ('email', 'last_name', 'first_name')
    list_filter = ('staff', 'admin',)
    list_display = ['email', 'full_name', 'staff', 'admin', 'is_active',]
    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('staff', 'admin', 'is_active',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('staff', 'admin',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
