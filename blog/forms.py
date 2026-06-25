import json
from django import forms
from .models import Blog
from django_ckeditor_5.widgets import CKEditor5Widget
import nh3
class CreateBlog(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        print(args)
        if args and args[0]:
            data = args[0].copy()  # Make raw POST data mutable
            raw_tags = data.get('tags', '').strip()
            
            if not raw_tags or raw_tags in ('[]', '""', "''"):
                data['tags'] = json.dumps([])
            elif not raw_tags.startswith('['):
                tag_list = [t.strip() for t in raw_tags.split(',') if t.strip()]
                data['tags'] = json.dumps(tag_list)
                
            args = (data,) + args[1:]  # Pass the fixed data back into the form

        super().__init__(*args, **kwargs)

        # 2. Convert database lists back into readable text tags on page load (Edit view)
        if self.instance and self.instance.pk and isinstance(self.instance.tags, list):
            self.fields['tags'].initial = ", ".join(self.instance.tags)
        elif self.fields['tags'].initial == []:
            self.fields['tags'].initial = ""
    class Meta:
        model = Blog
        fields = ("blog_title", "blog_summary", "cover_image", "blog_content", "category", "tags", "is_published")
        labels={"is_published":"Publish the blog"}
        widgets = {
            "blog_title": forms.TextInput(attrs={
                "class": "premium-input", 
                "id": "blog-title-input",
                "placeholder": "Enter a catchy title..."
            }),
            "blog_summary": forms.Textarea(attrs={
                "class": "premium-input premium-textarea", 
                "id": "blog-summary-input",
                "placeholder": "Write a short summary of your blog post...",
                "rows": 3
            }),
            "cover_image": forms.FileInput(attrs={
                "class": "premium-file-input", 
                "id": "blog-cover-input"
            }),
            "blog_content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, 
                config_name="extends"
            ),
            # NEW: Explicit styling target for category dropdown selection
            "category": forms.Select(attrs={
                "class": "premium-input premium-select",
                "id": "blog-category-select"
            }),
            # NEW: Render JSONField as a text input for user-friendly comma entry
            "tags": forms.TextInput(attrs={
                "class": "premium-input",
                "id": "blog-tags-input",
                "placeholder": "e.g. tech, tutorials, lifestyle"
            }),
            "is_published": forms.CheckboxInput(attrs={
                "class": "premium-toggle", 
                "id": "blog-publish-toggle"
            })
        }

    def clean_blog_content(self):
        raw_html = self.cleaned_data.get('blog_content')

        if not raw_html:
            return raw_html


        ckeditor_tags = {

            'p', 'br', 'hr', 'span', 'div',
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'strong', 'b', 'em', 'i', 'u', 's', 'strike', 'sub', 'sup', 'mark',


            'blockquote', 'pre', 'code',
            'ul', 'ol', 'li',


            'a',


            'table', 'thead', 'tbody', 'tr', 'th', 'td', 'caption',


            'img', 'figure', 'figcaption'
        }


        ckeditor_attributes = {

            '*': {'class', 'style', 'dir', 'lang'},


            'a': {'href', 'title', 'target', 'rel'},


            'th': {'scope', 'rowspan', 'colspan'},
            'td': {'rowspan', 'colspan'},

            # Images
            'img': {'src', 'alt', 'width', 'height', 'srcset'}
        }


        cleaned_html = nh3.clean(
            raw_html,
            tags=ckeditor_tags,
            attributes=ckeditor_attributes,

            url_schemes={'http', 'https', 'mailto'},
            link_rel=None
        )

        return cleaned_html