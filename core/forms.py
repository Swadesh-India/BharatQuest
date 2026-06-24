from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields='__all__'
        exclude=['created_at']
        widgets={
        'name':forms.TextInput(attrs={
        'class':'form-input',
        'placeholder':'username',
        'id':'name'
            
        }),
        'email':forms.EmailInput(attrs={
        'class':'form-input',
        'placeholder':'username@domain.com',
        'id':'email'
            
        }),
        'subject':forms.TextInput(attrs={
        'class':'form-input',
        'placeholder':'subject...',
        'id':'subject'
            
        }),
        'message':forms.TextInput(attrs={
        'class':'form-input',
        'placeholder':'message...',
        'id':'message'
            
        })
        }
       
        
        
        
        
        
        