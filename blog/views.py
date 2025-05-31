from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse , Http404
from django.contrib.auth.models import User
from django.urls import reverse
import logging
from .models import Post
from django.core.paginator import Paginator  # corrected import
from .form import ContactForm , RegisterForm , LoginForm , ForgotPasswordForm , ResetPasswordForm , PostForm
from .models import AboutUs 
from django.contrib.auth import authenticate ,login as authLogin , logout as auth_logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .models import Category
from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from .models import Post  # make sure Post model is imported

def index(request):
    all_posts = Post.objects.all()
    paginator_post = Paginator(all_posts, 5)  # corrected class name
    page_number = request.GET.get('page')
    page_object = paginator_post.get_page(page_number)  # fixed method call

    blog_title = 'Latest Posts'
    return render(request, 'blog/index.html', {
        'blog_title': blog_title,
        'post': page_object
    })


def detail(request,slug):
    #post_details = next((item  for item in  posts if item['id']==int(post_id)  ),None)
    try:
        post_details =  Post.objects.get(slug=slug)
        related_post = Post.objects.filter(category=post_details.category).exclude(pk=post_details.id)
    except Post.DoesNotExist:
        raise Http404("post Doesn't Exit")
    return render(request,'blog/detail.html',{"post":post_details , "related_post":related_post})


    

def old_url_redirect(request):
    return redirect(reverse('blog:new_page_url'))

def new_url_view(request):
    return HttpResponse('this is new URl')


def contact_view(request):
    
    # if request.method == 'POST':
    #     form = ContactForm(request.POST)
    #     name=request.POST.get('name')
    #     email=request.POST.get('email')
    #     message=request.POST.get('message')
    #     if form.is_valid():
    #         form.cleaned_data['name']
    #         success_message="You are email has been sent"
    #         return render(request,'blog/contact.html',{"form":form,'success_message':success_message})
    #         #sent in mail
    #     else:
    #         pass
    #     return render(request,'blog/contact.html',{"form":form,"name":name,"email":email,"message":message,})
       

    # return render(request,'blog/contact.html')
     if request.method == 'POST':
        form = ContactForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # logger = logging.getLogger("TESTING")
        if form.is_valid():
            # logger.debug(f'POST Data is {form.cleaned_data['name']} {form.cleaned_data['email']} {form.cleaned_data['message']}')
            #send email or save in database
            success_message = 'Your Email has been sent!'
            return render(request,'blog/contact.html', {'form':form,'success_message':success_message})
        else:
            # logger.debug('Form validation failure')
            return render(request,'blog/contact.html', {'form':form, 'name': name, 'email':email, 'message': message})
     return render(request,'blog/contact.html')

def about_view(request):
            about_content=AboutUs.objects.first().content   
            return render(request,'blog/about.html',{"about_content":about_content})



def register(request):
     message=''
     form = RegisterForm()
     if request.method == 'POST':
          form = RegisterForm(request.POST)
          if form.is_valid():
               user = form.save(commit=False)#user data save panum
               user.set_password(form.cleaned_data['password'])
               user.save()
               message='User register Successfully'
               return redirect('/login')

     return render(request,'blog/register.html',{"form":form,'message':message})
     
def login(request):
     form = LoginForm()
     if request.method =='POST':
          form = LoginForm(request.POST)
          if form.is_valid():
               username=form.cleaned_data['username']
               password=form.cleaned_data['password']
               user = authenticate(username=username,password=password)
               if user is not None:
                    authLogin(request,user)
                    return redirect('/dashboard')
                    
              
     return render(request,'blog/login.html',{'form':form})

def dashboard(request):
     blog_title='My Post'
     #geting suer post
     all_post=Post.objects.filter(user=request.user)
     paginator_post = Paginator(all_post, 5)  # corrected class name
     page_number = request.GET.get('page')
     page_object = paginator_post.get_page(page_number)  # fixed method call

     return render(request,'blog/dashboard.html',{'blog_title':blog_title,'page_object':page_object})

def logout(request):
     auth_logout(request)
     return redirect('blog:index')


def forgot_password(request):
     
    form = ForgotPasswordForm()
    if request.method == 'POST':
        #form
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            #send email to reset password
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            domain = current_site.domain
            subject = "Reset Password Requested"
            message = render_to_string('blog/reset_password.html', {
                'domain': domain,
                'uid': uid,
                'token': token
            })

            send_mail(subject, message, 'noreply@jvlcode.com', [email])

    return render(request,'blog/forgot_password.html',{'form':form})

def reset_password(request,uidb64,token):
     form=ResetPasswordForm()
     if request.method == "POST":
          form= ResetPasswordForm(request.POST)
          if form.is_valid():
               new_password=form.cleaned_data['new_password']
               try:
                    
                uid=urlsafe_base64_decode(uidb64)
                user=User.objects.get(pk=uid)
               except(TypeError,ValueError,OverflowError,User.DoesNotExist ):
                    user=None
                    
               if user is not None and default_token_generator.check_token(user,token):
                    user.set_password(new_password)
                    user.save()
                    print('changed')
                    return redirect('blog:login')
               else:
                    print('error')

     return render(request,"blog/reset_passwords.html",{'form':form})

@login_required
def new_post(request):

     form=PostForm()
     if request.method == "POST":
          form = PostForm(request.POST)
          if form.is_valid():
               post = form.save()
               post.user =request.user
               post.image_url='https://picsum.photos/id/17/800/400'
               post.save()

               return redirect('blog:dashboard')

     categories=Category.objects.all()
     return render(request,'blog/new_post.html',{"categories":categories,'form':form})


def edit_post(request,post_id):
     form=PostForm()
     categories=Category.objects.all()
     post = get_object_or_404(Post,id=post_id)
     if request.method =='POST':
          form = PostForm(request.POST,instance=post)
          if form.is_valid():
               form.save()

               return redirect('blog:dashboard')



     return render(request,'blog/edit_post.html',{'categories':categories,"post":post,'form':form})


def delete_post(request,post_id):
     post=get_object_or_404(Post,id=post_id)
     post.delete()
     return redirect('blog:dashboard')

     