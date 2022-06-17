import imp
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib import messages
from . import forms
import pickle
import pandas as pd
from Mpr import settings
# import pyrebase
# Create your views here.
from .models import updation

config = {
    'apiKey': "AIzaSyBMRDmmZ2pxOrdUaUC24hrkCj_rR7B6-J8",
    'authDomain': "creditcardfraud-380e6.firebaseapp.com",
    'databaseURL': "https://creditcardfraud-380e6.firebaseio.com",
    'projectId': "creditcardfraud-380e6",
    'storageBucket': "creditcardfraud-380e6.appspot.com",
    'messagingSenderId': "753300428318",
    'appId': "1:753300428318:web:c0df4357401ce1381e000f"
  }

# firebase=pyrebase.initialize_app(config)
# database=firebase.database()
# authe=firebase.auth()
# user={}

def index(request):
    global user
    try:
        context={
        'name':user['name']
        }
        return render(request,'base.html',context)
    except:
        return render(request,'base.html')

def Signin(request):
    my_form= forms.OnlyForm()

    if request.method== "POST":
        my_form=forms.OnlyForm(request.POST)
        if my_form.is_valid():
            print(my_form.cleaned_data)
            try:
                global user
                user=authe.sign_in_with_email_and_password(my_form.cleaned_data['email'],my_form.cleaned_data['password'])
                request.session['uid']=str(user['idToken'])
                print(user)
                name=my_form.cleaned_data['name']
                user['name']=name
                context={
                'name':name
                }
                return render(request,'base.html',context)
            except:
                message="Invalid Log-In Credentials!"
                context={
                'message':message,
                'form':my_form
                }
                return render(request,'signin.html',context)
        else:
            my_form.errors()
    context={
    'form':my_form
    }
    return render(request,'signin.html',context)

def Signup(request):
    my_form= forms.OnlyForm()

    if request.method== "POST":
        my_form=forms.OnlyForm(request.POST)
        if my_form.is_valid():
            print(my_form.cleaned_data)
            try:
                user=authe.create_user_with_email_and_password(my_form.cleaned_data['email'],my_form.cleaned_data['password'])
                authe.send_email_verification(user['idToken'])
                uid=user['localId']
                name=my_form.cleaned_data['name']
                email=my_form.cleaned_data['email']
                password=my_form.cleaned_data['password']
                data={'email':email,'name':name,'password':password}
                database.child("users").child(uid).child("details").set(data)
                messages.success(request,"Successfully Registered! Verify by logging your email")
            except:
                messages.error(request,"Email already taken :( ")
                print("error")
        else:
            my_form.errors()
    context={
    'form':my_form,
    }
    return render(request,'signup.html',context)

def Get_result(request):
    # print(settings.BASE_DIR)
    d = updation.objects.filter().order_by('-created')
    bas = settings.BASE_DIR
    bas = bas.replace("\\","/")
    name = str(d[0].uploading)
    final_url = bas+"/upload/"+name
    print(final_url)

    dataset = pd.read_csv("D:/Credit-Card-Fraud-Detection-master/Credit_Card_Applications.csv")
    d=pd.read_csv(final_url).to_html()
    html=dataset.to_html()

    
    try:
        context={
        'html':html,
        'f':d,
        'name':user['name']
        }
        return render(request,'results.html',context)
    except:
        context={
        'html':html,
        'f':d,
        }
        return render(request,'results.html',context)

def Working(request):
    try:
        context={
        'name':user['name']
        }
        return render(request,'working.html',context)
    except:
        return render(request,'working.html')


def Upload(request):
    try:
        context={
        'name':user['name']
        }
        return render(request,'upload1.html',context)
    except:
        return render(request,'upload1.html')


def Logout(request):
        auth.logout(request)
        global user
        user.clear()
        return render(request,'base.html')


def upload_file(request):
    if request.method == "POST":
        doc = request.FILES.getlist('myfile') #returns a dict-like object
        for d in doc:
            data = updation.objects.create(uploading=d)
            data.save()
        return redirect("result")
    return HttpResponse("error")