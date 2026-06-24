from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

   
class UserManager(BaseUserManager):
    def create_user(self,email, password=None,**extra_fields):
        if not email:
            raise ValueError("Please provide a valid email")
        user = self.model(email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.is_author = True

        user.save(using=self._db)
        return user

    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
      
        if extra_fields.get("is_staff") is not True :
            raise ValueError("superuser must have is_staff True")
        if extra_fields.get("is_superuser") is not True :
            raise ValueError("superuser must have is_superuser True")
        
        user = self.create_user(email, password,**extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.is_author = True

        user.save(using=self._db)
        return user



        

        

class User(AbstractBaseUser):
    username= models.CharField(max_length=30, unique=True)
    fullname=models.CharField(max_length=100)
    email = models.EmailField( max_length=254, unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_author = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS= ["username","fullname"]
    objects = UserManager()
    @property
    def first_name(self):
        return self.fullname.split(" ")[0] if self.fullname else ""
    
    def __str__(self):
        return self.username
    
    def has_perm(self,perms,obj=None):
        return self.is_superuser
    
    def has_module_perms(self,app_label):
        return self.is_superuser
    
    @property
    def get_role(self):
        if self.is_superuser:
            return "Admin"
        elif self.is_author:
            return "Author / Creator"
        else:
            return "Anonymous"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, help_text="A short bio about yourself.")
    dob = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    
    avatar = models.ImageField(
        upload_to='avatars/', 
        default='avatars/default_avatar.png', 
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time this profile was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="The date and time this profile was last updated.")

    def __str__(self):
        return f"{self.user.username}'s Profile"
