from django.contrib import admin

# Register your models here.
from .models import Complaint, Grievance

admin.site.register(Complaint)
admin.site.register(Grievance)
