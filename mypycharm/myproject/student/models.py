from django.db import models
from myapp.models import Teacher

class Student(models.Model):
    student_id = models.IntegerField(primary_key=True)
    student_name = models.CharField(max_length=100)
    attendance = models.IntegerField()
    percentage = models.FloatField()
    department = models.CharField(max_length=50)

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    risk = models.CharField(max_length=10, null=True, blank=True)
    alert_sent = models.BooleanField(default=False)
    alert_count = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=[
            ("ONGOING", "Ongoing"),
            ("IMPROVED", "Improved"),
            ("CRITICAL", "Critical"),
        ],
        default="ONGOING"
    )

    def __str__(self):
        return self.student_name

class Counselling(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    notes = models.TextField()
    recommendation = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.student.student_name