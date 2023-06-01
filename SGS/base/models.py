from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class Complaint(models.Model):
    STATUS = ((1,'Solved'),(2, 'InProgress'),(3,'Pending'))
    TYPE = (('Faculty', 'Faculty'), ('Academics', 'Academics'), 
            ('Canteen', 'Canteen'), ('Examination', 'Examination'), 
            ('Fees', 'Fees'), ('Hostel', 'Hostel'), ('Transport', 'Transport'),
            ('Management', 'Management'), ('Other', 'Other'))
    TO = (('CIVIL HOD', 'CIVIL HOD'),('CSE HOD', 'CSE HOD'), 
          ('ECE HOD', 'ECE HOD'), ('ECM HOD', 'ECM HOD'),
          ('EEE HOD', 'EEE HOD'), ('IT HOD', 'IT HOD'), 
          ('MECH HOD', 'MECH HOD'), ('MBA HOD', 'MBA HOD'),
          ('MANAGEMENT', 'MANAGEMENT') ,('PRINCIPLE', 'PRINCIPLE'),
          ('DIRECTOR', 'DIRECTOR'), ('CEO', 'CEO'))
    FROM_Branch = (('CIVIL', 'CIVIL'), ('CSE', 'CSE'), ('ECE', 'ECE'), 
                   ('ECM','ECM'), ('EEE', 'EEE'), ('IT','IT'), ('MBA', 'MBA'),
                   ('MECH', 'MECH'))


    id = models.AutoField(blank=False, primary_key=True)
    Subject=models.CharField(max_length=200,blank=False,null=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(default=datetime.now, blank=True)
    Type_of_complaint=models.CharField(choices=TYPE,null=True,max_length=200)
    To = models.CharField(choices=TO,null=True,max_length=200)
    From_Branch = models.CharField(choices=FROM_Branch,null=True,max_length=200)
    Description=models.TextField(max_length=4000,blank=False,null=True)
    status=models.IntegerField(choices=STATUS,default=3)

    def __init__(self, *args, **kwargs):
        super(Complaint, self).__init__(*args, **kwargs)
        self.__status = self.status

    def save(self, *args, **kwargs):
        if self.status and not self.__status:
            self.active_from = datetime.now()
        super(Complaint, self).save(*args, **kwargs)
    
    def __str__(self):
     	return self.get_Type_of_complaint_display()
    
class Grievance(models.Model):
    guser=models.OneToOneField(User,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return self.guser
    
class Admin(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    username = models.CharField(max_length=30, blank=True, unique=True)
    designation = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True,blank=True)
    # phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    
    def __str__(self):
        return self.username
    
    
