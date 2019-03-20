from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from forms import createTaskForm, createCategoryForm, createSettingsForm, createUserSettingsForm,PasswordChangeCustomForm,UserCreationCustomForm
from datetime import datetime,timedelta
from django.contrib.auth.decorators import login_required
from models import Category,Task,UserProfile
from django.contrib import messages
from random import choice
from string import ascii_lowercase, digits

def user_login(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('view_tasks'))

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            username = User.objects.get(email = email)
        except User.DoesNotExist:
            return render(request,'taskdesk/login.html',{'error': "Invalid login details"})

        user = authenticate(username = username, password = password)

        if user:
            if user.is_active:
                login(request,user,backend='django.contrib.auth.backends.ModelBackend')
                return HttpResponseRedirect(reverse('view_tasks'))
            else:
                return render(request,'taskdesk/login.html',{'error': "Your TaskDesk account is disabled"})
        else:
            return render(request,'taskdesk/login.html',{'error': "Invalid login details"})
    else:
        return render(request,'taskdesk/login.html',{})

def about_us(request):
    return render (request, 'taskdesk/about-us.html')
def faq(request):
    return render (request, 'taskdesk/faq.html')

def differenceInDaysFromToday(date):
    return int((date - datetime.today().date()).days)

@login_required
def deleteTask(request,task_id):
    Task.objects.filter(user=request.user, id=task_id).delete()
    return redirect(reverse('view_tasks'))

@login_required
def deleteCategory(request,category_id):
    Category.objects.filter(user=request.user, id=category_id).delete()
    return redirect(reverse('view_categories'))


def markAsDoneTask(request,task_id):
    task = Task.objects.get(user=request.user, id=task_id)
    task.done = True
    task.save()
    return redirect(reverse('view_tasks'))

def markAsNotDone(request,task_id):
    task = Task.objects.get(user=request.user, id=task_id)
    task.done = False
    task.save()
    return redirect(reverse('view_tasks'))

@login_required
def view_tasks(request, category_id=''):
    tasks = Task.objects.filter(user = request.user, done = False).order_by('personal_due_date','due_date','priority_level')
    category = None
    categorySet = False
    if(category_id!=''):
        category = Category.objects.filter(user = request.user, id = category_id).first()
        tasks = tasks.filter(category=category_id)
        categorySet = True

    Profile,created= UserProfile.objects.get_or_create(user = request.user)

    if created:
        c = Category.objects.create(user = request.user, category_name ='Test category - 1', category_description ='Test category - 1 - description')
        c2 = Category.objects.create(user = request.user, category_name ='Test category - 2')
        twoDaysInfuture = (datetime.now() + timedelta(days=2))
        twoDaysInPast = (datetime.now() + timedelta(days=-2))
        tomorrow = (datetime.now() + timedelta(days=1))


        Task.objects.create(user = request.user, category = c,task_name='Task Example 1',
        task_description="Task Description example 1",due_date=tomorrow,
        personal_due_date=twoDaysInPast,priority_level=3)
        Task.objects.create(user = request.user,
         category = c2,task_name='Task Example 2',
         due_date =twoDaysInfuture,personal_due_date=tomorrow,priority_level=1)


    if request.GET.get('cateogory'):
        tasks.filter(category=request.GET.get('cateogory'))

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

    return render(request,'taskdesk/view_tasks.html', {'tasks':tasks,'category':category,'categorySet':categorySet,'created':created})

@login_required

def manageTasks(request):
    tasks = Task.objects.filter(user = request.user)
    return render(request, 'taskdesk/view_all_tasks.html',{'tasks':tasks})

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
def editTask(request,task_id):
    instance = Task.objects.filter(user = request.user, id = task_id).first()
    if instance == None:
        return HttpResponseRedirect(reverse('view_tasks'))

    form = createTaskForm(request, request.POST or None, instance=instance)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('view_tasks'))

    return render(request, 'taskdesk/create_task.html', {'form': form,'edit':True,'task':instance})

@login_required
def view_categories(request):
    categories = Category.objects.filter(user = request.user)
    return render(request, 'taskdesk/view_categories.html',{'categories':categories})

@login_required
def editCategory(request,category_id):
    instance = Category.objects.filter(user = request.user, id = category_id).first()
    if instance == None:
        return HttpResponseRedirect(reverse('view_categories'))

    form = createCategoryForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('view_categories'))

    return render(request, 'taskdesk/create_category.html', {'form': form,'edit':True,'category':instance})

@login_required
def createCategory(request):
    category = createCategoryForm()

    if request.method == "POST":
        category = createCategoryForm(request.POST)

        if category.is_valid():
            category = category.save(commit = False)
            category.user = request.user
            category.save()
            return HttpResponseRedirect(reverse('view_categories'))
        else:
            print(category.errors)

    context_dict = {'form':category}

    return render(request,'taskdesk/create_category.html',context_dict)

@login_required
def userPersonalizeSettings(request):
    instance = UserProfile.objects.filter(user = request.user).first()

    form = createSettingsForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('userPersonalizeSettings'))

    return render(request, 'taskdesk/settings.html', {'form':form})


@login_required
def userAccountSettings(request):
    instance = request.user

    form = createUserSettingsForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('userAccountSettings'))

    return render(request, 'taskdesk/settings.html', {'form':form,'accountSettings':True})

@login_required
def userChangePassword(request):

    if request.method == 'POST':
        form = PasswordChangeCustomForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('userChangePassword')
        else:
            messages.error(request, 'Please correct the error below.')
    else:

        form = PasswordChangeCustomForm(request.user)

    return render(request, 'taskdesk/settings.html', {
        'form': form,'changePasword':True
    })
@login_required
def userDeleteAccount(request):
    to_delete = request.user
    to_delete.delete()
    return redirect(reverse('login'))

def generate_random_username(length=12, chars=ascii_lowercase+digits, split=3, delimiter='-'):

    username = ''.join([choice(chars) for i in xrange(length)])

    if split:
        username = delimiter.join([username[start:start+split] for start in range(0, len(username), split)])

    try:
        User.objects.get(username=username)
        return generate_random_username(length=length, chars=chars, split=split, delimiter=delimiter)
    except User.DoesNotExist:
        return username;

def register(request):
    if request.method == 'POST':
        form = UserCreationCustomForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=form.cleaned_data['username'])
            login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect(reverse('login'))
    else:
        form = UserCreationCustomForm(initial={'username': generate_random_username()})
    return render(request, 'taskdesk/registration.html', {'form': form})

def redirectToLogin(request):
    return redirect('login/')

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('login'))
