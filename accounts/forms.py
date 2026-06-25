from .models import User,Profile
from django import forms
from django.contrib.auth import authenticate
from datetime import date
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from django.core.cache import cache
# 1. Administrative & Staff Roles
ADMIN_USERNAMES = [
    'admin', 'administrator', 'root', 'superuser', 'sysadmin', 
    'system', 'webmaster', 'owner', 'manager', 'staff', 
    'moderator', 'mod', 'editor', 'author'
]

# 2. Support, Security & Corporate Communication
SUPPORT_USERNAMES = [
    'support', 'help', 'helpdesk', 'contact', 'info', 'service',
    'billing', 'sales', 'security', 'abuse', 'noreply', 'feedback'
]


ROUTING_USERNAMES = [
    'login', 'logout', 'signin', 'signup', 'register', 'join',
    'settings', 'profile', 'dashboard', 'account', 'about', 'home',
    'terms', 'privacy', 'search', 'api', 'static', 'media', 'index',
    'explore', 'blog', 'feed', 'notifications', 'messages', 'chat'
]


TECHNICAL_USERNAMES = [
    'bot', 'test', 'tester', 'guest', 'anonymous', 'user', 'member',
    'null', 'undefined', 'void', 'ftp', 'localhost', 'dev', 'developer'
]

BRAND_USERNAMES = [
    'bharatquest', 'bharat_quest', 'official', 'team', 'staff', 
    'verified', 'update', 'news','blog','blogs'
]


FORBIDDEN_USERNAMES = set(
    ADMIN_USERNAMES + 
    SUPPORT_USERNAMES + 
    ROUTING_USERNAMES + 
    TECHNICAL_USERNAMES + 
    BRAND_USERNAMES
)
class Register_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request_obj = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': ' ',
            'autocomplete': 'new-password',
            'id': 'id_confirm_password',
        })
    )
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class":"phone_number","value":"","autocomplete":"off","tabindex":"-1"})
    )
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(
            attrs={'class': 'form-input'} # You can pass custom classes if needed
        )
    )
   
    class Meta:
        model = User
        fields =["fullname","username","email","password"]
        widgets = {
            "username": forms.TextInput(attrs={
                
                'class': 'form-input',
                'placeholder': ' ', # Keeps your floating label trick working if you use CSS :placeholder-shown
                'autocomplete': 'off',
                'id': 'name',
                "minlength":"3",
              
            }),
            "fullname": forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': ' ',
                'autocomplete': 'name', # Helps browsers autofill real names
                'id': 'full_name',
                "minlength":"3",
            }),
            
            # 3. EMAIL FIELD
            "email": forms.EmailInput(attrs={ # Generates type="email" automatically
                'class': 'form-input',
                'placeholder': ' ',
                'autocomplete': 'email',
                'id': 'email',
            }),
            "password": forms.PasswordInput(attrs={ # Generates type="password" automatically
                'class': 'form-input',
                'placeholder': ' ',
                'autocomplete': 'new-password', # Prompts password managers to suggest a secure string
                'id': 'password',
                 "minlength":"5",
            }),
        }
    def clean(self):
        
        cleaned_data = super().clean()
        honey_pot= cleaned_data.get("phone_number")
        if honey_pot:
            
            x_forwarded_for = self.request_obj.META.get("HTTP_X_FORWARDED_FOR")
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0].strip()
            else:
                ip = self.request_obj.META.get("REMOTE_ADDR")
            
            cache.set(f"BANNED_IP_{ip}", True, 86400 * 7)
            self.add_error("username",f" { cleaned_data.get('email') } :BOT flagged")

        password_val = cleaned_data.get("password")
        cnf_password_val = cleaned_data.get("confirm_password")
        email_val = cleaned_data.get("email")
        user_name = cleaned_data.get("username")
        full_name = cleaned_data.get("fullname")
        
        if user_name and user_name.lower() in FORBIDDEN_USERNAMES:
            self.add_error("username","This username is not allowed")
        if full_name and full_name.lower() in FORBIDDEN_USERNAMES:
            self.add_error("fullname","This name is not allowed")
        if password_val and cnf_password_val :
            if  (password_val != cnf_password_val):
                self.add_error("confirm_password","Password is inappropriate")

                
        if User.objects.filter(username=user_name).exists():
            self.add_error("username","user name already exists")
        if User.objects.filter(email=email_val).exists():
            self.add_error("email","email already exists")


        return cleaned_data
       
      


class Login_form(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': ' ',
            'autocomplete': 'off',
            'id': 'name',      
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': ' ',
            'autocomplete': 'off', 
            'id': 'password',
        })
    )
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(
            attrs={'class': 'form-input'}
        )
    )




class Password_forget_form(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': ' ',
            'autocomplete': 'off',
            'id': 'name',      
        })
    )



class Password_reset_for_logged_in_form(forms.ModelForm):
  
    
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': ' ',
            'autocomplete': 'off', 
            'id': 'old_password',
        }),label="Old password",
    )
    confirm_new_password =forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': ' ',
            'autocomplete': 'off', 
            'id': 'confirm_new_password',
        }),label="Confirm password"
    )
    class Meta:
        model = User
        fields=["password"]
        widgets={
             "password": forms.PasswordInput(attrs={ # Generates type="password" automatically
                'class': 'form-input',
                'placeholder': ' ',
                'autocomplete': 'new-password', # Prompts password managers to suggest a secure string
                'id': 'password',
                 "minlength":"5",
             })
        }
        labels={
            "pasword":"New Password"
        }
       
    def clean(self):
        cleaned_data= super().clean()
        
        new_password= cleaned_data.get("password")
        confirm_new_password= cleaned_data.get("confirm_new_password")
        
        if new_password and confirm_new_password:
    
            if new_password!=confirm_new_password:
                self.add_error("new_password","password and confirm password didn't match")
        else:
            self.add_error("new_password","password not found")

        return cleaned_data
    


class Password_forget_reset_form(forms.ModelForm):
    confirm_password =forms.CharField(
            widget=forms.PasswordInput(attrs={
                'class': 'form-input',
                'placeholder': ' ',
                'autocomplete': 'off', 
                'id': 'confirm-password',
            }),label="Confirm password"
        )
    class Meta:
        model = User
        fields=["password"]
        widgets = {
             "password": forms.PasswordInput(attrs={
                'class': 'form-input',
                'placeholder': ' ',
                'autocomplete': 'new-password', 
                'id': 'password',
                 "minlength":"5",
            }),
        }
    def clean(self):
        cleaned_data= super().clean()
        password= cleaned_data.get("password")
        confirm_password= cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password!=confirm_password:
                self.add_error("password","password and confirm password didn't match")
        else:
            self.add_error("password","password not found")

        return cleaned_data
    
    def save(self,commit=True):
        user=self.instance
        print(self.cleaned_data.get("password")+"form")
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
        return user
    
class Account_activation_form(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': ' ',
            'autocomplete': 'off',
            'id': 'name',      
        })
    )




class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=["avatar","bio","dob"]
        widgets={
            "avatar": forms.FileInput(attrs={
                "class":"avatar-input"
            }),
            "bio":forms.TextInput(attrs={
                "class":"bio-input"
            }),
            "dob":forms.DateInput(attrs={
                "class":"dob-input",
                "type":"date"
            })
        }
    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data.get("dob")

        if dob:
            today = date.today()
            
            # 1. Prevent impossible future dates
            if dob > today:
                self.add_error('dob', "Date of birth cannot be in the future.")
            else:
                # 2. Calculate the exact age 
                # The boolean expression (...) evaluates to 1 if they haven't had their birthday yet, or 0 if they have.
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                
                # 3. Enforce the 4-year minimum
                if age < 4:
                    # Using add_error attaches the message directly to the input field in the HTML
                    self.add_error('dob', "You must be at least 4 years old to create a profile.")

        return cleaned_data