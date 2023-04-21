from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from fund import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token
import pandas as pd
import numpy as np
import pickle
from joblib import load
model=load(r"C:\Users\Jebon Lewis\OneDrive\Desktop\hackathon\fund\models\model.job")
modellog=load(r"C:\Users\Jebon Lewis\OneDrive\Desktop\hackathon\fund\models\modellog.job")
#modelforest=load(r"C:\Users\Jebon Lewis\OneDrive\Desktop\hackathon\fund\models\modelforest.job")
modelann=load(r"C:\Users\Jebon Lewis\OneDrive\Desktop\hackathon\fund\models\ANN_financialFraud.job")
modeldtree=load(r"C:\Users\Jebon Lewis\OneDrive\Desktop\hackathon\fund\models\DTree_financialFraud.job")
#data={"step":1,"amount":9839,"oldbalanceOrg":170136,"newbalanceOrig":16092,"oldbalanceDest":0,"newbalanceDest":0,"isFlaggedFraud":0}
#from sklearn.externals import joblib

# Create your views here.
dataset=""
mod=""
def home(request):
    return render(request, "homepage.html")
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('signup')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('signup')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('signup')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('signup')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        # Welcome Email
        subject = "Welcome to team annova Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to GFG!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\team anova"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ GFG - Django Login!!"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()
        
        return redirect('signin')
        
        
    return render(request, "signup.html")


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            username = user.username
            messages.success(request, "Logged In Sucessfully!!")
            return render(request, "index.html",{"username":username})
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('signin')
    
    return render(request, "signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')

def landing(request):
    return render(request,'landing.html')
def transaction(request):
    unimp=[]
    imp=[]
    global pred
    pred=3
    if request.method=="POST":
        tran=0
        """ date=request.POST.get("date")
        time=request.POST.get("time")
        nameori=request.POST.get("nameorgin")
        namedest=request.POST.get("namedest")"""
        amount=request.POST.get("amount")
        oldbalorg=request.POST.get("oldbalorg")
        newbalorg=request.POST.get("newbalorg")
        oldbaldest=request.POST.get("oldbaldest")
        newbaldest=request.POST.get("newbaldest")
        transaction=request.POST.get("transaction")
        hourofday=request.POST.get("hourofday")
        if transaction =="PAYMENT":
            tran=3
        elif transaction =="TRANSFER":
            tran=4
        elif transaction =="CASH-OUT":
            tran=1
        elif transaction =="DEBIT":
            tran=2
        elif transaction =="CASH-IN":
            tran=0
        print("amount",type(amount))
        print("oldborg",oldbalorg)
        print("newborg",newbalorg)
        print("oldbdest",oldbaldest)
        print("newbaldest",newbaldest)
        print("hourofday",hourofday)
        print("tran",tran)
        amount=float(amount)
        oldbalorg=float(oldbalorg)
        newbalorg=float(newbalorg)
        oldbaldest=float(oldbaldest)
        newbaldest=float(newbaldest)
        tran=float(tran)
        print(type(amount))
        #pred=modellog.predict([[amount,oldbalorg,newbalorg,oldbaldest,newbaldest,tran]])
        #pred=model.predict([[1,181.00,181.00,0.0,21182.00,0.00,0,1]])
        #pred=model.predict([[1,amount,oldbalorg,newbalorg,oldbaldest,newbaldest,0,tran]])
        if dataset=="dataset1" and mod=="logistic":
            print("log")
            pred=modellog.predict([[amount,oldbalorg,newbalorg,oldbaldest,newbaldest,tran]])
        elif dataset=="dataset1" and mod=="Dtrees":
            print("forest")
            hourofday=float(hourofday)
            pred=modeldtree.predict([[amount,oldbalorg,newbalorg,oldbaldest,newbaldest,hourofday,tran]])
        elif dataset=="dataset1" and mod=="Ann":
            hourofday=request.POST.get("hourofday")
            print("Ann")
            hourofday=float(hourofday)
            #pred=modelann.predict([[61237,0,0,88295,149533,19,1]])
            pred=modelann.predict([[amount,oldbalorg,newbalorg,oldbaldest,newbaldest,hourofday,tran]])
        elif dataset=="dataset2" and mod=="Dtrees":
            print("forest")
            #pred=modelforest.predict([[amount,oldbalorg,newbalorg,oldbaldest,newbaldest,tran]])
        elif dataset=="dataset2" and mod=="logistic":
            print("forest")
            pred=modellog.predict([[amount,oldbalorg,newbalorg,oldbaldest,newbaldest,1,tran]])
            print(pred)
        if pred==0:
            p="not fraud"
        elif pred==1:
            p="fraud"
        return render(request,'transaction_field.html',{'p':p,'dataset':dataset})
    return render(request,'transaction_field.html',{'mod':mod})
def adminlogin(request):
    return render(request,'adminLogin.html')

def demo(request):
    return render(request,"demo.html")

def dash(request):
    global dataset
    global mod
    if request.method=="POST" and request.POST.get('set'):
        dataset=request.POST["dataset"]
        mod=request.POST["model"]
        print(mod)
        print(dataset)
        return redirect('transaction')  
   
    username = request.user.username
    return render(request,'index.html',{'username':username})

def subscribe(request):
    return render(request,"subscribe.html")