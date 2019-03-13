from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from forms import createTaskForm, createCategoryForm
from datetime import datetime
from django.contrib.auth.decorators import login_required
from models import Category,Task,UserProfile

def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            username = User.objects.get(email = email)
        except User.DoesNotExist:
            return HttpResponse("Invalid login details supplied.")

        user = authenticate(username = username, password = password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('view_tasks'))
            else:
                return HttpResponse("Your TaskDesk account is disabled.")
        else:
            print("Invalid login details: {0},{1}".format(email,password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request,'taskdesk/login.html',{})

def about_us(request):
    return HttpsRe

def differenceInDaysFromToday(date):
    return int((date - datetime.today().date()).days)

def deleteTask(request,task_id):
    Task.objects.filter(user=request.user, id=task_id).delete()
    return redirect(reverse('view_tasks'))

def markAsDoneTask(request,task_id):
    task = Task.objects.get(user=request.user, id=task_id)
    task.done = True
    task.save()
    return redirect(reverse('view_tasks'))

def view_tasks(request):
    tasks = Task.objects.filter(user = request.user, done = False).order_by('personal_due_date','due_date')
    Profile,created= UserProfile.objects.get_or_create(user = request.user)

    for task in tasks:

        task.due_date_in_days = differenceInDaysFromToday(task.due_date)

        if(task.due_date_in_days < -1 or task.due_date_in_days > 1 ):
            day_or_days = ' days'
        else:
            day_or_days = ' day'
        if(task.due_date_in_days <= -1):
            task.due_date_message = str(abs(task.due_date_in_days)) + day_or_days + ' ago'
        else:
            task.due_date_message = 'In ' + str(task.due_date_in_days) + day_or_days


        if(task.personal_due_date):
            task.personal_due_date_in_days = differenceInDaysFromToday(task.personal_due_date)

            if(task.personal_due_date_in_days < -1 or task.personal_due_date_in_days > 1 ):
                day_or_days = ' days'
            else:
                day_or_days = ' day'

            if(task.personal_due_date_in_days <= -1):
                task.personal_due_date_message = str(abs(task.personal_due_date_in_days)) + day_or_days + ' ago'
            else:
                task.personal_due_date_message = 'In ' + str(task.personal_due_date_in_days) + day_or_days

        if task.priority_level == 1:
            task.priority_level = Profile.high_priority_color
        elif task.priority_level == 2:
            task.priority_level = Profile.medium_priority_color
        elif task.priority_level == 3:
            task.priority_level = Profile.low_priority_color

    return render(request,'taskdesk/view_tasks.html', {'tasks':tasks})
@login_required
def createTask(request):

    task = createTaskForm(request)

    if request.method == "POST":
        task = createTaskForm(request,request.POST)

        if task.is_valid():
            task = task.save(commit = False)
            task.user = request.user
            task.save()
            return HttpResponseRedirect(reverse('view_tasks'))
        else:
            print(task.errors)

    context_dict = {'form':task}
    return render(request,'taskdesk/create_task.html',context_dict)

@login_required
def createCategory(request):
    category = createCategoryForm()

    if request.method == "POST":
        category = createCategoryForm(request.POST,request.FILES)

        if category.is_valid():
            category = category.save(commit = False)
            category.user = request.user
            category.save()
            return HttpResponse("Added")
        else:
            print(category.errors)

    context_dict = {'form':category}

    return render(request,'taskdesk/create_category.html',context_dict)

def redirectToLogin(request):
    return redirect('login/')

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('login'))
