from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    name=models.CharField(max_length=100,null=True)
    email=models.EmailField(null=True)
    username=models.CharField(max_length=100,null=True,blank=True)
    password=models.CharField(max_length=100,null=True,blank=True)
    studentId=models.IntegerField(null=True)
    def __str__(self):
        return str(self.studentId)
class Notes(models.Model):
    user=models.ForeignKey(Student,on_delete=models.CASCADE)
    noteId=models.IntegerField(null=True,blank=True)
    title =models.CharField(max_length=200)
    description=models.TextField()
    def __str__(self):
        return self.title


class Homework(models.Model):
    user= models.ForeignKey(Student,on_delete=models.CASCADE)
    homeworkId=models.IntegerField(null=True,blank=True)
    subject=models.CharField(max_length=50)
    title= models.CharField(max_length=100)
    description=models.TextField()
    due=models.DateTimeField()
    fil=models.FileField(upload_to='',blank=True,null=True)
    is_finished=models.BooleanField(default=False)
    def __str__(self):
        return self.title
    
class Youtube(models.Model):
    user= models.ForeignKey(Student,on_delete=models.CASCADE)
    def __str__(self):
        return self.title
class Todo (models.Model):
    user=models.ForeignKey(Student,on_delete=models.CASCADE)
    todoId=models.IntegerField(null=True)
    title=models.CharField(max_length=100)
    date=models.DateField(blank=True,null=True)
    desc=models.CharField(max_length=200,blank=True)
    is_finished=models.BooleanField(default=False)
    def __str__(self):
        return self.title
    