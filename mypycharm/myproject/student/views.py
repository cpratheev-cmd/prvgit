from django.shortcuts import render, redirect, get_object_or_404
from student.models import Student,Counselling
from myapp.models import Teacher
from django.core.mail import send_mail
from django.conf import settings
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

def calculate_risk(attendance, percentage):
    score = (attendance * 0.4) + (percentage * 0.6)
    if score < 50:
        return score, "HIGH"
    elif score < 70:
        return score, "MEDIUM"
    else:
        return score, "LOW"

def student_dashboard(request):
    sid = request.session.get("student_id")
    if not sid:
        return redirect('student:login')
    student = Student.objects.get(student_id=sid)
    score, risk = calculate_risk(
        student.attendance,
        student.percentage
    )
    student.risk = risk
    if risk == "HIGH" and not student.alert_sent:
        send_teacher_alert(student)
        student.alert_sent = True
    student.save()
    recommendation = generate_recommendation(student)
    return render(request, "student_dashboard.html", {
        "student": student,
        "risk": risk,
        "score": round(score, 1),
        "recommendation": recommendation
    })
def high_risk_students(request):
    teacher_id = request.session.get("teacher_id")
    students = Student.objects.filter(
        teacher_id=teacher_id,
        risk="HIGH"
    )
    return render(request, "high_risk_students.html", {"students": students})
def medium_risk_students(request):
    teacher_id = request.session.get("teacher_id")
    students = Student.objects.filter(
        teacher_id=teacher_id,
        risk="MEDIUM"
    )
    return render(request, "medium_risk_students.html", {"students": students})

def low_risk_students(request):
    teacher_id = request.session.get("teacher_id")
    students = Student.objects.filter(
        teacher_id=teacher_id,
        risk="LOW"
    )
    return render(request, "low_risk_students.html", {"students": students})

def add_student(request):
    if request.method == "POST":
        teacher_id = request.session.get("teacher_id")
        teacher = Teacher.objects.get(uid=teacher_id)
        attendance = int(request.POST['attendance'])
        percentage = float(request.POST['percentage'])
        score, risk = calculate_risk(attendance, percentage)
        Student.objects.create(
            student_id=request.POST['student_id'],
            student_name=request.POST['student_name'],
            attendance=attendance,
            percentage=percentage,
            department=request.POST['department'],
            risk=risk,
            teacher=teacher
        )
        return HttpResponse("Student record saved successfully")
    return render(request, "teacher_dashboard.html")

def view_students(request):
    teacher_id = request.session.get("teacher_id")
    students = Student.objects.filter(teacher_id=teacher_id)
    search_query = request.GET.get("search")
    if search_query:
        students = students.filter(student_name__icontains=search_query)
    risk_filter = request.GET.get("risk")
    if risk_filter:
        students = students.filter(risk=risk_filter)
    status_filter = request.GET.get("status")
    if status_filter:
        students = students.filter(status=status_filter)
    return render(request, "view.html", {
        "students": students
    })

def edit_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == "POST":
        student.student_name = request.POST['student_name']
        student.attendance = int(request.POST['attendance'])
        student.percentage = float(request.POST['percentage'])
        student.department = request.POST['department']

        score, risk = calculate_risk(
            student.attendance,
            student.percentage
        )
        student.risk = risk
        student.save()

        if risk == "HIGH":
            send_teacher_alert(student)
        return redirect('student:view_students')
    return render(request, "edit.html", {"student": student})

def delete_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    student.delete()
    return redirect('student:view_students')

def student_logout(request):
    request.session.flush()
    return redirect('new')

def send_teacher_alert(student):

    teacher = student.teacher
    if not teacher or not teacher.email:
        return
    subject = "🚨 High Risk Student Alert"
    message = f"""
Warning!
Student Name: {student.student_name}
Student ID: {student.student_id}
Attendance: {student.attendance}%
Percentage: {student.percentage}%
Department: {student.department}
Risk Level: HIGH
Please take immediate action.
"""
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [teacher.email],
        fail_silently=False
    )
    student.alert_count += 1
    student.save()

def alert_dashboard(request):
    teacher_id = request.session.get("teacher_id")
    students = Student.objects.filter(
        teacher_id=teacher_id
    ).order_by("-alert_count")
    max_alert = students.first().alert_count if students.exists() else 0
    return render(request, "alert_dashboard.html", {
        "students": students,
        "max_alert": max_alert
    })

def generate_recommendation(student):
    suggestions = []
    if student.attendance < 60:
        suggestions.append("Improve attendance immediately.")
    if student.percentage < 50:
        suggestions.append("Focus on academic improvement.")
    if student.risk == "HIGH":
        suggestions.append("Meet counselor and parents.")
    if not suggestions:
        suggestions.append("Good performance. Keep maintaining consistency.")
    return " ".join(suggestions)

def counselling_page(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    teacher_id = request.session.get("teacher_id")
    teacher = Teacher.objects.get(uid=teacher_id)
    if request.method == "POST":
        notes = request.POST.get("notes")
        recommendation = request.POST.get("recommendation")
        status = request.POST.get("status")

        Counselling.objects.create(
            student=student,
            teacher=teacher,
            notes=notes,
            recommendation=recommendation
        )
        student.status = status
        student.save()
        return redirect("student:view_students")
    return render(request, "counselling.html", {
        "student": student
    })

def counselling_history(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    records = Counselling.objects.filter(student=student).order_by("-date")
    return render(request, "counseling_dashboard.html", {
        "student": student,
        "records": records
    })