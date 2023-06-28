from django.contrib import admin
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Like

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "gender",
                    "profile",
                    "img_preview",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "first_name", "last_name", "password1", "password2"),
            },
        ),
    )
    list_display = ['email', 'name' ,'first_name', 'last_name', 'is_staff']
    search_fields = ('email', 'name')
    readonly_fields = ['img_preview']
    ordering = ('email', )

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'publish']
    
    # def get_name(self, obj):
    #     return obj.user.first_name.title() if obj.user.first_name else '--'
    # get_name.short_description = 'USER NAME'     
    
@admin.register(Like)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'post']
    
    # def get_name(self, obj):
    #     return obj.user.first_name.title() if obj.user.first_name else '--'
    # get_name.short_description = 'USER NAME'     