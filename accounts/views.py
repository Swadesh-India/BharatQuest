from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash


from .tokens import activation_token_generator,deletion_token_generator
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str,force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode

from django.contrib.sites.shortcuts import get_current_site

from .utils import send_user_verification_email
from django.utils.html import strip_tags
from django.template.loader import render_to_string

from django.http import HttpResponseForbidden
from .forms import Register_form,Login_form,Password_forget_form,Password_forget_reset_form,Password_reset_for_logged_in_form,Account_activation_form,ProfileForm
from .models import User,Profile

from .decorators import valid_reset_session_required, limit_submission_rate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django_ratelimit.decorators import ratelimit

@ratelimit(key="ip", rate="10/m", method='POST', block=True)
@ratelimit(key="post:email",rate="5/m", method='POST', block=False)
@limit_submission_rate(seconds=10)
def login_view(request):
    
    if request.user.is_authenticated:
        return redirect("home")
    if request.method=='POST':
        if getattr(request,"limited",False):
            messages.error(request, "You have requested too many login attempts. Please try again in a minute.")
            return redirect("login")
        
        form = Login_form(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
          
            myus= User.objects.filter(email=email).first()
            print(email)
            obj=None
            if myus is not None and myus.check_password(password):
            
                if myus.is_active:
                    print("yes sir")
                    obj = authenticate(request, username=email,password=password)
                else:
                    messages.error(request, "Your account is inactive. So it can't be logged in. To activate your account, refer to the Login Help section", extra_tags="validation")
                    return render(request, 'accounts/login.html',{"form":form})
            if obj is not None:
                last_login = obj.last_login
                login(request,obj)
                messages.success(request,"Login successfull")
                if last_login is None:
                    return redirect("edit-profile")
                return redirect("home")
            else:
                messages.error(request,"login failed. Invalid credentials") 
        else:
            messages.error(request,"login failed")
    else :
        form = Login_form()

        
    
    return render(request, 'accounts/login.html',{"form":form})

@ratelimit(key="ip",rate="5/m", method='POST', block=False)
@limit_submission_rate(seconds=10)
def registration_view(request):
    if request.method=='POST':
        if getattr(request,"limited",False):
            messages.error(request, "You have requested too many pregistration attempts. Please try again in a minute.")
            return redirect("register")
        form = Register_form(request.POST, request=request)
        if form.is_valid():
            

            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            username = form.cleaned_data.get("username")
            fullname = form.cleaned_data.get("fullname")
            
           
            user = User.objects.create_user(
                email=email, 
                password=password, 
                username=username, 
                fullname=fullname,
                is_active=False
            )
            current_site = get_current_site(request)
            context = {
        "user":user,
        "uid":urlsafe_base64_encode(force_bytes(user.pk)),
        "domain":current_site.domain,
        
        "token":activation_token_generator.make_token(user)

    }
            subject = 'Activate Your Account'
            html_message = render_to_string('accounts/registration/activation_email.html', context)
            plain_message =strip_tags(html_message)
            send_user_verification_email(request=request,
                user=user,
                subject=subject,
                html_message=html_message,
                plain_message=plain_message,
                type="activate")


            return redirect("login")
        else:
            if request.POST.get("phone_number"):
                return HttpResponseForbidden("Your IP is flagged as spam")
            messages.error(request,"Failed to create account")
    else :
        form = Register_form()
        
     
    return render(request, 'accounts/register.html',{"form":form})

@ratelimit(key="ip", rate="5/m", method=ratelimit.ALL,block=True)
@limit_submission_rate(seconds=10)
def activation_view(request, uidb, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb))
        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user is not None and activation_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request, "Your email has been verified successfully! You can now log in.")
        return redirect("login")
    else:
        return render(request, 'accounts/registration/activation_invalid.html')

@login_required(login_url="/accounts/login")
@limit_submission_rate(seconds=1)
def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('login')

@limit_submission_rate(seconds=10)
@ratelimit(key="ip",rate="5/m", method='POST', block=False)
@ratelimit(key="post:email", rate="3/m", method='POST', block=False)
def password_forget_view(request):
    if request.method=="POST":
        if getattr(request,"limited",False):
            messages.error(request, "You have requested too many password resets. Please try again in a minute.")
            return redirect("password-forget")
        form = Password_forget_form(request.POST)
       
        if  form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.filter(email=email).first()
            if user is not None:

                current_site = get_current_site(request)
                context = {
        "user":user,
        "uid":urlsafe_base64_encode(force_bytes(user.pk)),
        "domain":current_site.domain,
        
        "token":default_token_generator.make_token(user)

    }
                subject ="Reset you password"
                html_message = render_to_string("accounts/forget/password-forget-email.html",context)
                plain_message= strip_tags(html_message)
                send_user_verification_email(request=request,subject=subject,user=user,html_message=html_message,plain_message=plain_message,type="reset")
                return redirect("password-forget")
            else:
                messages.error(request,"Some error occured")
                return redirect("password-forget")
    else:
        form = Password_forget_form()
    return render(request,"accounts/password_forget.html",{"form":form})

@valid_reset_session_required
@limit_submission_rate(seconds=10)
def password_reset_view(request):

    if request.method == "POST":
  
        user_id = request.session.get("reset_user_id")
        user = User.objects.filter(pk=user_id).first()
        if not request.user.is_authenticated:
            form = Password_forget_reset_form(request.POST,instance=user)
        else:
            form = Password_forget_reset_form(request.POST)

        if user is not None:
          
            if form.is_valid(): 
                request.session.pop('reset_user_id', None)
                if not request.user.is_authenticated:
                    form.save()
                else:
                    password=form.cleaned_data.get("password")
                    request.user.set_password(password)
                    request.user.save()
                    update_session_auth_hash(request,request.user)
                    messages.success(request, "Password updated successfully!")
                    return redirect("home")
                messages.success(request,"password reset successfully")
                return redirect("login")
            else:
                messages.error(request,"Failed, to reset password")
        
    else:
        form = Password_forget_reset_form()
    return render(request,"accounts/forget/password_forget_reset.html",{"form":form})

@ratelimit(key="ip", rate="5/m", method=ratelimit.ALL,block=True)
def reset_password_view(request,uidb,token):
    user = None
    try:
        uid = force_str(urlsafe_base64_decode(uidb))
        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user is not None and default_token_generator.check_token(user,token):

        request.session['reset_user_id'] = user.pk
        messages.success(request, "Your email has been verified successfully! You can now reset your password.")
        return redirect("password-reset")
    else:
        return render(request, 'accounts/forget/password_reset_invalid.html')
    




@login_required
@limit_submission_rate(seconds=10)
@ratelimit(key="user",rate="5/m", method="POST", block=False)
def password_reset_for_logged_in(request):
    
    if request.method=="POST":
            if getattr(request,"limited",False):
                messages.error(request, "You have requested too many password reset. Please try again in a minute.")
                return redirect("password-reset-for-logged-in")
            form = Password_reset_for_logged_in_form(request.POST)
            
            if form.is_valid():
                old_password= form.cleaned_data.get("old_password")
                new_password= form.cleaned_data.get("password")
                if (not old_password) or (not new_password):
                    messages.error(request,"Password not found")
                    return render(request,"accounts/forget/password-reset-for-logged-in.html",{"form":form})
                    
                if request.user.check_password(old_password) :
                    request.user.set_password(new_password)
                    request.user.save()
                    update_session_auth_hash(request,request.user)
                    messages.success(request, "Password updated successfully!")
                    return redirect("home")
                else:
                    messages.error(request,"Old password didn't match")
    else:
        form = Password_reset_for_logged_in_form()
    return render(request,"accounts/forget/password-reset-for-logged-in.html",{"form":form})


@login_required
@require_POST
@limit_submission_rate(seconds=10)
@ratelimit(key="user", rate="5/m", method="POST", block=True)
def delete_account_request(request):
    email = request.user.email

    current_site = get_current_site(request)
    context = {
"user":request.user,
"uid":urlsafe_base64_encode(force_bytes(request.user.pk)),
"domain":current_site.domain,
"token":deletion_token_generator.make_token(request.user)

}
    subject ="Account Delete confirmation"
    html_message = render_to_string("accounts/delete-account-email.html",context)
    plain_message= strip_tags(html_message)
    send_user_verification_email(request=request,subject=subject,user=request.user,html_message=html_message,plain_message=plain_message,type="delete")
    return redirect("home")


@ratelimit(key="ip", rate="5/m", method=ratelimit.ALL,block=True)
def delete_account_confirm(request,uidb,token):
    user = None
    try:
        uid = force_str(urlsafe_base64_decode(uidb))
        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user is not None and deletion_token_generator.check_token(user,token):
        logout(request)
        user.delete()
        messages.success(request, "Your account deleted successfully! ")
        return redirect("home")
    else:
        return render(request, 'accounts/delete_account_invalid.html')
    
@limit_submission_rate(seconds=10)
@ratelimit(key="ip", rate="5/m", method=ratelimit.ALL,block=True)
def account_activation_later(request):
    if request.method=="POST":
        form = Account_activation_form(request.POST)
       
        if  form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.filter(email=email).first()
            if user is not None:

                current_site = get_current_site(request)
                context = {
        "user":user,
        "uid":urlsafe_base64_encode(force_bytes(user.pk)),
        "domain":current_site.domain,
        
        "token":activation_token_generator.make_token(user)

    }
            
                subject = 'Activate Your Account'
                html_message = render_to_string('accounts/registration/activation_email.html', context)
                plain_message =strip_tags(html_message)
                send_user_verification_email(request=request,
                    user=user,
                subject=subject,
                html_message=html_message,
                plain_message=plain_message,
                type="activate_later")
            else:
                messages.error(request,"Some error occured")
                return render(request,"accounts/activate-account-later.html",{"form":form})
    else:
        form = Account_activation_form()
    return render(request,"accounts/activate-account-later.html",{"form":form})


@login_required
@limit_submission_rate(seconds=10)
def profile_view(request):
    user_profile= Profile.objects.filter(user=request.user).first()

    if request.method=="POST":
        form = ProfileForm(request.POST,request.FILES,instance=user_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user=request.user
            profile.save()
            return redirect("home")
    else:
        form = ProfileForm(instance=user_profile)
    
    return render(request, "accounts/edit-profile.html",{"form":form})