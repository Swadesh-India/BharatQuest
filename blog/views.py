from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import models
from .forms import CreateBlog
from .decorators import author_perms_reqired
def blogs(request):
    featured_blogs=models.Blog.objects.filter(is_featured=True,is_published=True)
    other_blogs=models.Blog.objects.filter(is_featured=False,is_published=True)
    
    
    return render(request, 'blog/blogs.html',{
        "featured_blogs":featured_blogs,
        'other_blogs': other_blogs,
        
    })


from django.db.models import F
def blog_detail(request,blog_id,slug):
    post = get_object_or_404(models.Blog, slug=slug, id=blog_id, is_published=True)
    session_key = f'viewed_post_{post.id}'
    if not request.session.get(session_key, False):
        models.Blog.objects.filter(id=post.id).update(views=F('views') + 1)
        request.session[session_key] = True
        post.refresh_from_db()
    blog_content= models.Blog.objects.filter(id=blog_id,slug=slug).first()
    
    return render(request, "blog/blogcontent.html",{"blog":blog_content})
@login_required(login_url="/accounts/login")
@author_perms_reqired
def add_blog(request):
    
    if request.method =="POST":
        form = CreateBlog(request.POST,request.FILES)
        if form.is_valid(): 
            blog=form.save(commit=False)
            blog.author=request.user
            blog.save()
            messages.success(request,"Blog added successfully")
            return redirect("myblogs")
        else:
            messages.error(request,"Blog is't added")

    else:
        form = CreateBlog()
    return render(request,"blog/addblog.html",{"form":form})

@login_required
@author_perms_reqired
def myblogs(request):
    blogs =request.user.blogs.all
    

   
    if not blogs :
        previous_url = request.META.get('HTTP_REFERER')
        if previous_url is not None:
            messages.error(request,"You have no blogs")
            return redirect(previous_url)   
        

    return render(request,"blog/myblogs.html",{"blogs":blogs})


@login_required
@author_perms_reqired
def edit_blog(request):
    blog_id = request.GET.get('blogId')
    slug = request.GET.get('slug')

    blog_instance = get_object_or_404(models.Blog, pk=blog_id, slug=slug)
    if request.method =="POST":
        form = CreateBlog(request.POST,request.FILES,instance=blog_instance)
        if form.is_valid(): 
            form.save()
            messages.success(request,"Blog Updated successfully")
            return redirect("myblogs")
        else:
            messages.error(request,"Blog is't Updated")

    else:
        messages.success(request, "Only modify those fields that you want to update")
        form = CreateBlog(instance=blog_instance)

    return render(request,"blog/addblog.html",{"form":form})