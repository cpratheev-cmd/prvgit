from django.db import models
class Student(models.Model):
    student_id = models.IntegerField(primary_key=True)
    student_name = models.CharField(max_length=100)
    attendance = models.IntegerField()
    percentage = models.FloatField()
    department = models.CharField(max_length=50)
    risk=models.CharField(max_length=50)
    def __str__(self):
        return self.student_name

