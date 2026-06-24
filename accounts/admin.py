from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class ModelAdmin(UserAdmin):
    model=User
    list_display =("email","username","fullname","is_staff","is_active","is_superuser")
    list_filter = ("is_superuser",)
    filter_horizontal = []

    search_fields = ["email", "username", "fullname"]
    ordering = ["email"]

   
    fieldsets = (
        ("credentials", {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("fullname", "username")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "is_author")}),
        ("Important dates", {"fields": ("last_login", "created_at", "updated_at")}),
    )

    readonly_fields = ["created_at", "updated_at"]
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password"),
        }),
    )


from .models import Profile

# Register your model so it shows up in the admin panel
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username',)