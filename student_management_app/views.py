from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from student_management_app.EmailBackEnd import EmailBackEnd
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.
def showDemopage(request):
    return render(request, "demo.html")

def showLoginpage(request):
    return render(request, 'login_page.html')

@ensure_csrf_cookie
def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = authenticate(request=request, username=request.POST.get("email"), password=request.POST.get("password"))
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/admin_home')
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect('/') # Render login page again

@ensure_csrf_cookie
def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User : "+request.user.email+" usertype : "+str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")

@ensure_csrf_cookie
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")
