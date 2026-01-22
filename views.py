from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from django.http import HttpResponse

def student_login(request):
    if request.method == "POST":
        sid = request.POST.get('student_id')
        print("SID RECEIVED:", sid)
        try:
            student = Student.objects.get(student_id=int(sid))
            request.session["student_id"] = student.student_id
            return redirect('student:student_dashboard')
        except Student.DoesNotExist:
            return HttpResponse("<h1>Student not found, Please try again</h1>")
    return render(request, "student_login.html")

def student_dashboard(request):
    sid = request.session.get("student_id")
    if not sid:
        return redirect('student:login')
    student = Student.objects.get(student_id=int(sid))
    return render(request, "student_dashboard.html", {"student": student})

def add_student(request):
    if request.method == "POST":
        Student.objects.create(
            student_id=request.POST['student_id'],
            student_name=request.POST['student_name'],
            attendance=request.POST['attendance'],
            percentage=request.POST['percentage'],
            department=request.POST['department'],
            risk=request.POST['risk'],
        )
        return HttpResponse("Student record saved successfully")
    return render(request, "teacher_dashboard.html")

def view_students(request):
    students = Student.objects.all()
    return render(request, "view.html", {"students": students})

def edit_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)

    if request.method == "POST":
        student.student_name = request.POST['student_name']
        student.attendance = request.POST['attendance']
        student.percentage = request.POST['percentage']
        student.department = request.POST['department']
        student.risk = request.POST['risk']
        student.save()
        return redirect('student:view_students')
    return render(request, "edit.html", {"student": student})
def delete_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    student.delete()
    return redirect('student:view_students')
def student_logout(request):
    request.session.flush()
    return redirect('new')
