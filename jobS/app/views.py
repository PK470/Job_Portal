from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import*
from .forms import ResumeForm,Cform
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

# Create your views here.
def register(request):
    
    if request.method == "POST":
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        employer = request.POST.get('option1')
        if pass1!=pass2:
            messages.success(request,'First and second passwords are not same')
            return render(request,'register.html')
        if User.objects.filter(username=uname).exists() or User.objects.filter(email=email).exists():
            messages.success(request,'Username or email already exists')
            return render(request, 'register.html')   

        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            if employer == 'Yes':
                juser = Juser.objects.create(user=my_user, name=uname, email=email,employer = True)
                juser.save()
            else:
                juser = Juser.objects.create(user=my_user, name=uname, email=email,employer=False)
                juser.save()
                
            #print(uname,email,pass1,pass2)
            return redirect('login')  
    return render(request,'register.html')

def ulogin(request):
    if request.method == "POST":
        uname = request.POST.get('uname')
        password = request.POST.get('password')
        
        user = authenticate(request, username=uname, password=password)
        
        if user is not None:
            login(request, user)
            juser = Juser.objects.get(user = user)
            if juser.employer:
                return redirect('cview')
            try:
                resume = Resume.objects.get(user=user)
                return redirect('home')
            except ObjectDoesNotExist:
                return redirect('upload_resume')
        else:
            messages.error(request, 'Please enter correct username or password')
            return render(request, 'login.html')

    return render(request, 'login.html')

def home(request):
    job = Job.objects.all()
    context = {'jobs':job}
    return render(request,'home.html',context)
def jview(request,pk):
        
        job = Job.objects.get(id=pk)
        
        
        context = {'job':job}
        print(job.id)
        return render(request,'view.html',context)
    
    
def upload_resume(request):
    try:
        if request.method == 'POST':
            form = ResumeForm(request.POST, request.FILES)
            if form.is_valid():
                resume = form.save(commit=False)
                resume.user = request.user  
                resume.save()
                return redirect('home') 
        else:
            form = ResumeForm()
    except:
        messages.success(request,'Something Wents wrong')
        return redirect('home')
    return render(request, 'personal.html', {'form': form})

def create_job(request):
    try:
        if request.method == 'POST':
            form = Cform(request.POST, request.FILES)
            if form.is_valid():
                job = form.save(commit=False)
                juser = Juser.objects.get(user = request.user)
                job.company = juser
                job.save()
                return redirect('cview') 
        else:
            form = Cform()
    except:
        messages.success(request,'Something Wents wrong')
        return redirect('cview')
    return render(request, 'create_job.html', {'form': form})

def apply(request,pk):
    user =  request.user
    job = Job.objects.get(id=pk)
    resume = Resume.objects.get(user = user)
    if Apply.objects.filter(user = user,job=job).exists():
        messages.success(request,"Already Applied")
        return redirect('home')
    else:
        apply= Apply.objects.create(job=job,user=user,resume=resume)
        apply.save()
        messages.success(request,"Applied")
    return render(request,'home.html')

def cview(request):
    user = request.user
    user = Juser.objects.get(user = user)
    if Job.objects.filter(company = user).exists():
        job = Job.objects.filter(company = user)
        print(job)
        context = {'jobs':job}
        return render(request,'cview.html',context)
    else:
        messages.success(request,'No jobs Posted Yet')
    return render(request,'cview.html')

def cjview(request,pk):
    job = Job.objects.get(id=pk)
    apply = Apply.objects.filter(job = job)
    context = {'jobs':job, 'applys':apply}
    return render(request,'cjview.html',context)
def uLogout(request):
    logout(request)
    return redirect('home')

def search(request):
    try:
        if request.method == 'POST':
            querry = request.POST.get('search')
            print(querry)
            job = Job.objects.filter((Q(title__icontains= querry)) | (Q(skills__icontains= querry)))
            if job.exists():
                context ={'jobs':job}
                return render(request,'home.html',context)
            else:
                messages.success(request,'No result Found')
                return redirect('home')
    except:
        messages.success(request,'No result Found')
        return redirect('home')
