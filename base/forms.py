from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Complaint
from django.core.exceptions import ValidationError
import re

# class statusupdate(forms.ModelForm):
#     class Meta:
#         model = Complaint
#         exclude = ['id', 'user', 'created', 'Subject', 'severity', 'status', 'Description', 'To', 'user_id','From_Branch', 'Type_of_complaint']

class statusupdate(forms.ModelForm):
    class Meta:
        model=Complaint
        fields = ("id", "status", "remarks")


class ComplaintForm(forms.ModelForm):

  def validate_complaint_message(self, message):
    unparliamentary_words = ['skjdlk', 'sidj', 'word3']
    regex_pattern = r'\b(' + '|'.join(unparliamentary_words) + r')\b'
    if re.search(regex_pattern, message, re.IGNORECASE):
      raise ValidationError('The complaint message includes unparliamentary words.')
    
  def clean_Description(self):
    description = self.cleaned_data.get('Description')
    self.validate_complaint_message(description)
    return description
    # def assign_priority(self, message):
    # priority_words = ['skjdlk', 'sidj', 'word2']
    # regex_pattern = r'\b(' + '|'.join(priority_words) + r')\b'
    # if re.search(regex_pattern, message, re.IGNORECASE):
    # raise ValidationError('The complaint message includes unparliamentary words.')
  # def assign_severity(complaint):
  # severity = None
  # if "urgent" in complaint.Description or "emergency" in complaint.Description:
  # severity = "High"
  # elif "important" in complaint.Description or "deadline" in complaint.Description:
  # severity = "Medium"
  # else:
  # severity = "Low"
  # return severity
  class Meta:
    model = Complaint
    fields = ('Type_of_complaint', 'To', 'From_Branch', 'Subject', 'Description')

class NewUserForm(UserCreationForm):
	# branch_choices = (('CIVIL', 'CIVIL'), ('CSE', 'CSE'), ('ECE', 'ECE'), 
    #                ('ECM','ECM'), ('EEE', 'EEE'), ('IT','IT'), ('MBA', 'MBA'),
    #                ('MECH', 'MECH'))

	email = forms.EmailField(required=True)
	first_name = forms.CharField(max_length=20, required=True)
	last_name = forms.CharField(max_length=20, required= True) 
	username = forms.CharField(max_length=20, required= True)       
	branch = forms.CharField(max_length=5, required=True)
	roll_no = forms.CharField(max_length=10, required= True) 
	college = forms.CharField(max_length=50, required= True) 
	
	class Meta:
		model = User
		# fields = ("first_name", "last_name", "username", "email", "college", "branch", "roll_no", "password1", "password2")
		fields = ("username", "email","password1")


	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

	

