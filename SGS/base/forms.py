from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Complaint,Admin


class ComplaintForm(forms.ModelForm):
    class Meta:
        model=Complaint
        fields=('Type_of_complaint', 'To', 'From_Branch', 'Subject','Description')

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
		fields = ("first_name", "last_name", "username", "email", "college", "branch", "roll_no", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user
	
class NewAdminForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(max_length=20, required=True)
	last_name = forms.CharField(max_length=20, required= True) 
	username = forms.CharField(max_length=20, required= True)       
	designation = forms.CharField(max_length=20, required=True)
	# phone_number=forms.PhoneNumberField()
	# roll_no = forms.CharField(max_length=10, required= True) 
	# college = forms.CharField(max_length=50, required= True) 

	class Meta:
		model = Admin
		fields = ("first_name", "last_name", "username", "email", "designation", "password1", "password2")

	def save(self, commit=True):
		user = super(NewAdminForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user
		
