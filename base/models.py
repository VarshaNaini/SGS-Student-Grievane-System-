from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from phonenumber_field.modelfields import PhoneNumberField



# Create your models here.


class Complaint(models.Model):
    STATUS = ((1,'Solved'),(2, 'InProgress'),(3,'Pending'),(4,'Escalated'))
    TYPE = (('Faculty', 'Faculty'), ('Academics', 'Academics'), 
            ('Canteen', 'Canteen'), ('Examination', 'Examination'), 
            ('Fees', 'Fees'), ('Hostel', 'Hostel'), ('Transport', 'Transport'),
            ('Management', 'Management'), ('Other', 'Other'))
    TO = (('CIVIL_HOD', 'CIVIL HOD'),('CSE_HOD', 'CSE HOD'), 
          ('ECE_HOD', 'ECE HOD'), ('ECM_HOD', 'ECM HOD'),
          ('EEE_HOD', 'EEE HOD'), ('IT_HOD', 'IT HOD'), 
          ('MECH_HOD', 'MECH HOD'), ('MBA_HOD', 'MBA HOD'),
          ('MANAGEMENT', 'MANAGEMENT') ,('PRINCIPLE', 'PRINCIPLE'),
          ('DIRECTOR', 'DIRECTOR'), ('CEO', 'CEO'))
    FROM_Branch = (('CIVIL', 'CIVIL'), ('CSE', 'CSE'), ('ECE', 'ECE'), 
                   ('ECM','ECM'), ('EEE', 'EEE'), ('IT','IT'), ('MBA', 'MBA'),
                   ('MECH', 'MECH'))


    id = models.AutoField(blank=False, primary_key=True, null=False)
    Subject=models.CharField(max_length=200,blank=False,null=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(default=datetime.now, blank=True)
    Type_of_complaint=models.CharField(choices=TYPE,null=True,max_length=200)
    To = models.CharField(choices=TO,null=True,max_length=200)
    From_Branch = models.CharField(choices=FROM_Branch,null=True,max_length=200)
    Description=models.TextField(max_length=4000,blank=False,null=True)
    remarks=models.TextField(max_length=4000, null=True)
    status=models.IntegerField(choices=STATUS,default=3)
    severity = models.CharField(max_length=50, blank=True, null=True)
    allocated_time = models.DurationField(blank=True, null=True)
    escalated = models.BooleanField(default=False)
    current_handler = models.CharField(max_length=100, blank=True, null=True)
    escalation_time = models.DateTimeField(blank=True, null=True)
    # deadline = models.DateTimeField()

    class Meta:
        ordering = ['-updated','-created','severity']

    def save(self, *args, **kwargs):
        if self.status and self.remarks:
            self.active_from = datetime.now()
        super(Complaint, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.severity:
            self.severity = self.calculate_severity()
        super().save(*args, **kwargs)

    # def calculate_severity(self):
    #     severity = "low"
    #     if "urgent" in self.Description or "emergency" in self.Description:
    #         severity = "High"
    #     elif "important" in self.Description or "deadline" in self.Description:
    #         severity = "Medium"
    #     else:
    #         severity = "Low"
    #     return severity
    
    def calculate_severity(self):
        severity = None
        if self.Description:
            if "urgent" in self.Description.lower() or "emergency" in self.Description.lower():
                severity = "High"
            elif "important" in self.Description.lower() or "deadline" in self.Description.lower():
                severity = "Medium"
            else:
                severity = "Low"
        return severity

    
    # def forward_to_next_authority(self):
    #     """
    #     This function forwards the complaint to the next higher authority.
    #     """
    #     if self.authority == 'HOD':
    #         self.authority = 'PRINCIPAL'
    #     elif self.authority == 'PRINCIPAL':
    #         self.authority = 'DIRECTOR'
    #     elif self.authority == 'DIRECTOR':
    #         self.authority = 'CEO'
    #     else:
    #         self.status = 'Closed'
    #     self.updated_at = timezone.now()
    #     self.save()
    
    def __str__(self):
         return self.get_Type_of_complaint_display()

    
    
class Grievance(models.Model):
    guser=models.OneToOneField(User,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return self.guser

    
# user = User.objects.create_user(username='username', password='password', email='email')
# user.save()


# https://writexo.com/265kcoo5
# https://writexo.com/265kcol5