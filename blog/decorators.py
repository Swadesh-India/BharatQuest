from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def author_perms_reqired(myfunc):

    @wraps(myfunc)
    def wrapper (request, *args, **kwargs):
        
        
        if not request.user.is_author:
            messages.error(request,"You are not an author. ")
            return redirect("blogs")
        return myfunc(request, *args, **kwargs)
    return wrapper
