from django.shortcuts import visitor_cookie_handler

def user_login(request):
    return render(request, 'taskdesk/login.html',{})
