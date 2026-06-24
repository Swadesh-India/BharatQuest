from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect

def valid_reset_session_required(myfunc):

    @wraps(myfunc)
    def wrapper (request, *args, **kwargs):
        
        session_user_id = request.session.get("reset_user_id")
        if not session_user_id:
            messages.error(request,"Invalid or expired password reset session. Please request a new link.")
            return redirect("password-forget")
        return myfunc(request, *args, **kwargs)
    return wrapper



from django.core.cache import cache
from django.http import HttpResponseForbidden

def limit_submission_rate(seconds=10):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Only apply rate limiting to POST requests (form submissions)
            if request.method == "POST":
                # Generate a unique cache key based on the user ID (or session key if anonymous)
                if request.user.is_authenticated:
                    user_key = f"rate_limit_form_{request.user.id}"
                else:
                    user_key = f"rate_limit_form_anon_{request.session.session_key or request.META.get('REMOTE_ADDR')}"
                
                # Check if the key exists in the cache
                if cache.get(user_key):
                     return HttpResponseForbidden("Please wait 10 seconds between form submissions.")
                # Set the key in the cache with the specified timeout duration
                cache.set(user_key, True, timeout=seconds)
                
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator