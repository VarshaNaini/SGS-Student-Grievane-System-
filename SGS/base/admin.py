from django.contrib import admin

# Register your models here.
from .models import Complaint, Grievance,Admin

admin.site.register(Complaint)
admin.site.register(Grievance)
admin.site.register(Admin)