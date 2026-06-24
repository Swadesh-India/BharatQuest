from django.contrib import admin

from . import models
class BlogAdmin(admin.ModelAdmin): 
    list_display = ("blog_title", "author", "blog_summary", "blog_content","is_featured", "is_published")
    list_editable = ('is_published', "is_featured")
    
    readonly_fields = ("author", "slug", "likes", "views")

    fieldsets = (
        ("Blog Content", {
            "fields": ("blog_title", "blog_summary", "blog_content", "cover_image")
        }),
        ("Publishing & Promotion", {
            "fields": ("is_published", "is_featured"),
            "classes": ("collapse",),  
        }),
        ("Author Details", {
            # Replaced author_id and author_name with author
            "fields": ("author",),
        }),
        ("Metrics & SEO", {
            "fields": ("slug", "views", "likes"),
            "classes": ("collapse",),  # Collapsed by default to keep things tidy
        }),
    )

    def save_model(self, request, obj, form, change):
        # Automatically assign the logged-in admin if no author exists
        if not hasattr(obj, 'author') or obj.author is None:  
            obj.author = request.user
            
        super().save_model(request, obj, form, change)

# Register using the new class name
admin.site.register(models.Blog, BlogAdmin)