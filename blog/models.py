from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth import get_user_model
User = get_user_model()
class Blog(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Technology'),
        ('lifestyle', 'Lifestyle'),
        ('travel', 'Travel & Adventure'),
        ('finance', 'Business & Finance'),
        ('education', 'Education & Tutorials'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
  
    slug = models.SlugField(blank=True)
    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    is_featured = models.BooleanField(default=False)
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='tech'
    )
    tags = models.JSONField(default=list,blank=True,null=True)

    blog_title = models.CharField(max_length=200)
    cover_image = models.ImageField(upload_to='blog_images',default="")
    blog_content = CKEditor5Field(max_length=10000,config_name="extends")
    blog_summary = models.TextField(max_length=255)
    comments = models.JSONField(default=list,blank=True)
    share= models.IntegerField(default=0)

   
    def save(self, *args,**kwargs):
        self.slug=slugify(self.blog_title)
        super().save(*args,**kwargs)
    
    def __str__(self):
        return self.blog_title