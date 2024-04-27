from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile


# Create your views here.


def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        user = User.objects.filter(username=email)
        if not user.exists():
            messages.warning(request,"Account Does Not Exist")
            return HttpResponseRedirect(request.path_info)
        if not user[0].profile.is_email_verified:
            messages.warning(request,"Your Account Is Not Verified")
            return HttpResponseRedirect(request.path_info)
        user = authenticate(username=email, password=pass1)
        if user:
            login(request,user)
            return redirect('/')
        messages.warning(request,"Invalid Credential")
        return HttpResponseRedirect(request.path_info)
    return render(request,'account/login.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if pass1 != pass2:
            messages.error(request, "Password Does Not Match")
            return HttpResponseRedirect(request.path_info)
        user = User.objects.filter(username = email)
        if user.exists():
            messages.error(request,"Email is Already Taken")
            return HttpResponseRedirect(request.path_info)
        user = User.objects.create(first_name=name, username=email, email=email, password=pass1)
        user.save()
        messages.success(request,"SignUp Successfully ! Please confirm your email address to complete the registration")
        return redirect('/account/login/')
    return render(request, 'account/register.html')


def activate_email_account(request, email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/account/login/')
    except Exception as e:
        return HttpResponse("<h1>Invalid Email Token</h1>")


