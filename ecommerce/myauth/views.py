from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# To active the user Account
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.urls import NoReverseMatch, reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str

# To send the Email to activate account
from django.core.mail import EmailMessage
# from django.core import mail
from django.conf import settings
from .token import account_activate_token

# Class Based View
from django.views import View

# Create your views here.
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']
        if password != confirm_password:
            messages.warning(request, "Password Does Not Match")
            return render(request, 'auth/signup.html')
        
        try:
            if User.objects.get(email=email):
                messages.error(request, "Given User Email Already Exist So, Please Give Different Email To SignUp")
                return render(request, 'auth/signup.html')
        except Exception as identifier:
            print(identifier)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()

        # To get the domain of the current site
        # e.g., -:   127.0.0.1:8000
        current_site = get_current_site(request)
        mail_subject = 'Activation link has been sent to your email id'
        message = render_to_string('auth/activate.html',{
            'user':user,
            'domain':current_site,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activate_token.make_token(user),
        })
        
        activate_email = EmailMessage(
            mail_subject, message,settings.EMAIL_HOST_USER, to=[email]
        )

        activate_email.send()

        messages.info(request, 'SignUp Successfully ! Please confirm your email address to complete the registration')
        return redirect('/auth/login/')
    return render(request, 'auth/signup.html')

def mylogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, 'Successfull Login')
            return redirect('/')
        else:
            messages.error(request, 'User Does Not Exist')
            return redirect('/auth/login/')
    return render(request, 'auth/login.html')

def mylogout(request):
    logout(request)
    return redirect('/auth/login/')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = uid)
    except Exception as identifier:
        user = None

    if user is not None and account_activate_token.check_token(user,token=token):
        user.is_active = True
        user.save()
        return redirect('/auth/login/')
    return HttpResponse("Something Went Wrong Try To signup Again")


# Class Based View In Django For Password Reset
class RequestResetEmailView(View):

    def get(self , request):
        return render(request, 'auth/reset_password.html')
    
    def post(self, request):
        email = request.POST['email']
        try:
            user = User.objects.filter(email=email)
            if user.exists():
                current_site = get_current_site(request)
                email_subject = "[Reset Your Password]"
                message = render_to_string('auth/link_reset_password.html',{
                    'user':user,
                    'domain':current_site,
                    'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                    'token':PasswordResetTokenGenerator().make_token(user[0]),
                })
                reset_email = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, to=[email])
                reset_email.send()
        except Exception as identifier:
            print(identifier)
        return redirect('/auth/login/')
    
class ResetPasswordView(View):
    def get(self, request,uidb64,token):
        context = {
            'uidb64':uidb64,
            'token':token,
        }
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(uid=uid)
            if not PasswordResetTokenGenerator.check_token(user, token=token):
                messages.warning(request,"Password Reset link is invalid !!")
                return render(request, 'auth/reset_password.html')
            
        except Exception as identifier:
            print(identifier)

        return render(request, 'auth/reset_done.html', context=context)
    
    def post(self, request, uidb64, token):
        context = {
            'uidb64':uidb64,
            'token':token,
        }
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']

        if password != confirm_password:
            messages.error(request, 'Password Does not match')
            return render(request, 'auth/reset_done.html', context=context)
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password Reset Successful, Please Login With New Password')
            return redirect('/auth/login/')
        except Exception as identifier:
            print(identifier)
            return render(request, 'auth/reset_done.html', context=context)
        
        return rende(request, 'auth/reset_done.html', context=context)
