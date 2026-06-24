from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_user_verification_email(request,user,subject='subject',html_message="html_message",plain_message="plain message",type="activate"): 
    if user is not None:
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            if type=="activate":
                messages.success(request, "Account created successfully! Please check your email to activate your account.",extra_tags="validation")
            elif type=="activate_later":
                messages.success(request, "Activation email sent successfully. Please check your email to activate your account.",extra_tags="validation")
            elif type=="reset":
                messages.success(request, "Password reset email sent successfully! Please check your inbox.",extra_tags="validation")
            elif type=="delete":
                messages.success(request, "Account deletion email sent successfully! Please check your inbox.",extra_tags="validation")
        
        
        except Exception as e:
            if type=="activate":
                logger.error(f"SMTP failure during registration for {user.email}: {e}")
                user.delete() 
                messages.error(request, "Failed to send activation email. Please check your network or try again later.")
            elif type=="reset":
                logger.error(f"SMTP failure during resetting password for {user.email}: {e}")
    
            elif type=="delete":
                logger.error(f"SMTP failure during deleting account for {user.email}: {e}")
            elif type=="activate_later":
                logger.error(f"SMTP failure during sending account activation email for {user.email}: {e}")
            else:
                logger.log("SMTP faliure")
    



import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
import os
# A curated palette of standard, vibrant colors (Hex codes)
AVATAR_COLORS = [
    "#F44336", "#E91E63", "#9C27B0", "#673AB7", 
    "#3F51B5", "#2196F3", "#03A9F4", "#00BCD4", 
    "#009688", "#4CAF50", "#8BC34A", "#FF9800", 
    "#FF5722", "#795548", "#607D8B"
]

def generate_initials_avatar(user):
    """
    Generates a circular avatar using the user's initials and a random 
    background color, then saves it to their Profile model.
    """
    # 1. Get the first letter of the full name, fallback to username
    name = user.fullname.strip()
    if not name:
        name = user.username
        
    first_letter = name[0].upper() if name else "?"

    # 2. Setup image dimensions and select a random color
    size = 256
    bg_color = random.choice(AVATAR_COLORS)
    
    # 3. Create a blank image with a transparent background (RGBA)
    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)


    draw.ellipse([0, 0, size, size], fill=bg_color)

    try:
        font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Roboto_Condensed-Medium.ttf')

        font = ImageFont.truetype(font_path, 150)
    except IOError:
       
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), first_letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) / 2
    y = (size - text_height) / 2 - bbox[1]

    draw.text((x, y), first_letter, fill="#FFFFFF", font=font)

    buffer = BytesIO()
    img.save(buffer, format="PNG")
   
    filename = f"{user.username}_avatar.png"
    
    if hasattr(user, 'profile'):
       
        user.profile.avatar.save(filename, ContentFile(buffer.getvalue()), save=True)
        return True
        
    return False