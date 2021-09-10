from typing import Type
from django.db.models.query import RawQuerySet
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages,auth
from django.contrib.auth import logout
from django.http import HttpResponse
from django.template import Context, Template, RequestContext, context
from . forms import ProfileUpdateForm
from resource.models import Article, Resource
# Email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required   
# Create your views here.

def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username = username).exists():
                messages.warning(request,'Username already exists')
                return redirect('register')
            else:
                if User.objects.filter(email = email).exists():
                    messages.warning(request,'Email already registered')
                    return redirect('register')

                else:
                    user = User.objects.create_user(
                        first_name = first_name,
                        last_name = last_name,
                        username = username,
                        email = email,
                        password = password,
                    )
                    
                    user.is_active = False
                    user.save()

                    # Email Verification

                    current_site = get_current_site(request)
                    mail_subject = "Please Activate Your Account"
                    context = {
                        'user': user,
                        'domain': current_site,
                        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                        'token':default_token_generator.make_token(user),
                    }
                    message = render_to_string('users/account_verification_email.html', context)

                    to_email = email
                    send_email = EmailMessage(mail_subject, message, to = [to_email])
                    send_email.send()

                    messages.success(request,'Email verification link sent')
                    return redirect('home')
        else:   
            messages.warning(request,"Password don't Match")
            return redirect('register')




    return render(request, 'users/register.html')


def login(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = username, password= password)
        if user is not None:
            auth.login(request,user)
            messages.success(request, "Login Success")
            return redirect('home')
        else:
            messages.warning(request, "Invalid Credentials")
            return redirect('login')


    return render(request,'users/login.html')

def logout_user(request):
    logout(request)
    messages.success(request,"You have been successfully logged out")
    return redirect('home')

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk = uid)
    except(TypeError, ValueError, OverflowError,User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Account Activated Successfully")
        return redirect('login')
    else:
        messages.error(request, "Invalid Link")
        return redirect('register')


# forgot password

def forgot_password(request):
    if request.method == "POST":
        email = request.POST['email']

        if User.objects.filter(email = email).exists():
            user = User.objects.get(email__exact =  email)
            current_site = get_current_site(request)
            mail_subject = "Password Reset"
            context = {
                'user': user,
                'domain': current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            }
            message = render_to_string('users/reset_password_email.html', context)

            to_email = email
            send_email = EmailMessage(mail_subject, message, to = [to_email])
            send_email.send()
            messages.success(request, "Password Reset Email Sent")
            return redirect('login')

        else:
            messages.error(request, "Account Does not Exists")
            return redirect('register')
    return render(request, 'users/forgot_password.html')

def forgot_password_validate(request, uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk = uid)
    except(TypeError, ValueError, OverflowError,User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please Reaset Your Password')
        return redirect('reset_password')
    else:
        messages.error(request, 'Link Expired')
    return redirect('login')


def reset_password(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk = uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password Reset Successfully")
            return redirect('login')

        else:
            messages.error(request, "Password do not match")
            return redirect('reset_password')
    else:
        return render(request, 'users/reset_password.html')

@login_required(login_url='login')
def profile(request):
    current_user = request.user
    articles_posted_by_user = Article.objects.filter(article_posted_by= current_user).order_by('-article_posted_on')
    resource_posted_by_user = Resource.objects.filter(resource_posted_by= current_user).order_by('-updated_on')
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST,instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Account Updates Succesfully !!!')
            return redirect('profile')
    else:
        profile_form = ProfileUpdateForm(instance=request.user)
    context = {
        'profile_form':profile_form,
        'articles_posted_by_user':articles_posted_by_user,
        'resource_posted_by_user':resource_posted_by_user,
    }
    return render(request, 'users/profile.html', context)


