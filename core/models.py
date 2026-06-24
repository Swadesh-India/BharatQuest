from django.db import models

class Contact(models.Model):
    name= models.CharField(max_length=60)
    email= models.EmailField(max_length=60)
    subject= models.CharField(max_length=100)
    message= models.TextField(max_length=255)
    created_at= models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} | {self.subject}"
    
# class TeamMember(models.Model):
#     name = models.CharField(max_length=60)
#     role = models.CharField(max_length=100, help_text="Designation or role (e.g., Proof Reader).")
#     img = models.ImageField(upload_to='team_photos/', 
#         blank=True, 
#         null=True, 
#         help_text="Profile picture of the team member.")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     social = 