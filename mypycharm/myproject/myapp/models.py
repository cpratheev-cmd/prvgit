from django.db import models
class Teacher(models.Model):
    uid=models.IntegerField(primary_key=True)
    pwd=models.CharField(max_length=20)
    dep=models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    def __str__(self):
        return str(self.uid)

