from django.shortcuts import render,redirect
from django.http import HttpResponse
from.models import Teacher
def new(request):
    return render(request, "new.html")
def teacher_register(request):
    if request.method == "POST":
        uid = request.POST['t1']
        if Teacher.objects.filter(uid=uid).exists():
            return HttpResponse("Teacher already registered")
        Teacher.objects.create(
            uid=uid,
            pwd=request.POST['t2'],
            dep=request.POST['t3'],
            email = request.POST['t4'],
        )
        return redirect('teacher_login')
    return render(request, "teacher_register.html")
def teacher_login(request):
    if request.method == "POST":
        uid = request.POST['t1']
        pwd = request.POST['t2']
        if Teacher.objects.filter(uid=uid, pwd=pwd).exists():
            request.session['teacher_id'] = uid
            return redirect('teacher_dashboard')
        else:
            return HttpResponse("<h1>You are not register Yet!...</h1><a href=/log/>back</a>")
    return render(request, "teacher_login.test.html")

def input(request):
    return render(request, "input.html")
def retun(request):
    return render(request, "new.html")
def teacher_dashboard(request):
    return render(request, "dashboard.html")

def logout(request):
    return HttpResponse("Logout Page (Coming Soon)")






