from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .forms import NewUserForm, ComplaintForm, statusupdate
from .models import Complaint
# from .tasks import test_func
from .tasks import escalate_complaint
from django.core.mail import EmailMessage
from datetime import datetime,timedelta
from django.conf import settings
# import datetime


# def test(request):
#     test_func.delay()
#     return HttpResponse("Done")

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('userdashboard')

    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.username=='CIVIL_HOD':
                    login(request, user)
                    return redirect('admindashboard')
            else:
                    login(request, user)
                    return redirect('userdashboard')
        else:
            messages.error(request, 'Username or password does not exist')
        
    return render(request, 'login.html')


def adminloginPage(request):
    if request.user.is_authenticated:
        return redirect('admindashboard')

    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.username[-3:]=='HOD' or user.username=='DIRECTOR' or user.username=='PRINCIPAL' or user.username=='CEO' or user.username=='MANAGEMENT':
                    login(request, user)
                    return redirect('admindashboard')
            else:
                    """login(request, user)
                    return redirect('userdashboard')"""
                    messages.error(request, 'Admin or password does not exist')
        else:
            messages.error(request, 'Username or password does not exist')
        
    return render(request, 'login.html')

@login_required
def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = NewUserForm()
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('userdashboard')
        else:
            messages.error(request, 'An Error occured during registration')
    return render(request, 'userregister.html', {'form':form})

def home(request):
    return render(request, 'home.html')

@login_required  
def userdashboard(request):
    complaints = Complaint.objects.all()
    context = {'complaints': complaints}
    return render(request, 'userdashboard.html', context)

@login_required
def lodge_complaint(request):
    form = ComplaintForm()
    if request.method == "POST":
        form = ComplaintForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user=request.user
            # instance.allocated_time = datetime.now() + settings.COMPLAINT_ALLOCATION_TIMES[instance.To] # Set the allocated time for the complaint object based on the responsible person's role
            # Get the current datetime
            # current_datetime = datetime.now()
            # # Add a time interval of 24 hours
            # allocated_time = current_datetime + timedelta(minutes=5)
            # # Set the allocated time for the complaint object
            instance.allocated_time = timedelta(minutes=5)
            instance.save()

            # Escalate the complaint to the next authority
            # escalate_complaint.delay(instance.pk)  # Pass the complaint ID as an argument to the task
            escalate_complaint.delay()
             # Schedule the task to check escalation after the allocated time
            # escalate_complaint.apply_async(args=[instance.id], eta=instance.allocated_time)

            # Send email to admin
            subject = 'New Complaint Lodged'
            message = 'A new complaint has been lodged by {} ({}). Please log in to the admin panel to view the details.'.format(request.user.username, request.user.email)
            from_email = request.user.email
            to_email = 'varsha.naini@gmail.com' # Replace with the admin's email address
            email = EmailMessage(subject, message, from_email, [to_email])
            email.send()

            messages.success(request, 'Complaint lodged Successfully')
            return redirect('userdashboard')
        else:
            messages.error(request, 'An Error occured during lodging the complaint or The complaint message includes unparliamentary words.')
            return redirect('lodgecomplaint')
    return render(request, 'lodge_complaints.html', {'form': form})

@login_required
def update_password(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('userdashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    
    context = {'form': form}
    return render(request, 'user_update_password.html', context)


def update_password1(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('admindashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    
    context = {'form': form}
    return render(request, 'admin update password.html', context)

@login_required
def complaint_status_Pending(request):
    complaints = Complaint.objects.filter(user = request.user).exclude(Q(status='1') | Q(status='2'))
    count = complaints.count()
    context={'complaints': complaints, 'count': count}
  
    if request.method == 'GET':
        return render(request, 'complaints_status_pending.html', context)

def pending(request):
    complaints = Complaint.objects.filter(To = request.user).exclude(Q(status='1') | Q(status='2'))
    count = complaints.count()
    context={'complaints': complaints, 'count': count}
    if request.method == 'GET':
        return render(request, 'pending.html', context)
    #return render(request, 'complaints_status_pending.html')
    

@login_required
def complaint_status_InProcess(request):
    complaints = Complaint.objects.filter(user = request.user).exclude(Q(status='1') | Q(status='3'))
    count = complaints.count()
    context={'complaints': complaints, 'count': count}
    if request.method == 'GET':
        return render(request, 'complaints_status_inprocess.html', context)
    # return render(request, 'complaints_status_inprocess.html', context)

def inprocess(request):
    complaints = Complaint.objects.filter(To = request.user).exclude(Q(status='1') | Q(status='3'))
    count = complaints.count()
    context={'complaints': complaints, 'count': count}
    if request.method == 'GET':
        return render(request, 'inprocess.html', context)
    # return render(request, 'complaints_status_inprocess.html', context)

@login_required
def complaint_status_Solved(request):
    complaints = Complaint.objects.filter(user = request.user).exclude(Q(status='2') | Q(status='3'))
    count = complaints.count()
    context={'complaints': complaints, 'count': count}
    if request.method == 'GET':
        return render(request, 'complaints_status_solved.html', context)
    # return render(request, 'complaints_status_solved.html', context)

def closed(request):
    complaints = Complaint.objects.filter(To = request.user).exclude(Q(status='2') | Q(status='3'))
    count = complaints.count()
    context={'complaints': complaints, 'count': count}
    if request.method == 'GET':
        return render(request, 'closed.html', context)
    # return render(request, 'complaints_status_solved.html', context)


@login_required
def complaint_status_All(request):
    complaints = Complaint.objects.filter(user = request.user)
    count = complaints.count()
    if request.method == 'GET':
        q = request.GET.get('q') if request.GET.get('q') != None else ''
        complaints = Complaint.objects.filter(user=request.user).filter(
        Q(id__icontains=q) |
        Q(Subject__icontains = q) |
        Q(Type_of_complaint__icontains = q) |
        Q(From_Branch__icontains = q) |
        Q(Description__icontains = q)
        )
        count = complaints.count()

    context={'complaints': complaints, 'count': count}
    return render(request, 'complaints_status_all.html', context)


def total(request):
    complaints = Complaint.objects.filter(To = request.user)
    count = complaints.count()
    if request.method == 'GET':
        # return render(request, 'total.html', context)
        q = request.GET.get('q') if request.GET.get('q') != None else ''
        complaints = Complaint.objects.filter(To=request.user).filter(
        Q(id__icontains=q) |
        Q(Subject__icontains = q) |
        Q(Type_of_complaint__icontains = q) |
        Q(From_Branch__icontains = q) |
        Q(Description__icontains = q)
        )
        count = complaints.count()
        
    context={'complaints': complaints, 'count': count}
    return render(request, 'total.html', context)


@login_required
def admindashboard(request):
    #complaints = Complaint.objects.all()
    #context = {'complaints': complaints}
    
   
    # if q!='':
    #     context = {'complaints': complaints, 'c_count': c_count}
    #     return redirect(request, 'abc.html', context)

    return render(request, 'admindashboard.html', context={})

def abc(request, context):
    return render(request, 'abc.html', context)

def viewdetails(request,id):
    complaint = Complaint.objects.filter(id=id)
    context={'complaint':complaint}
    if request.method=='GET':
        return render(request,'viewdetails.html',context)

# def adminviewdetails(request,id):
#     complaint = Complaint.objects.filter(id=id)
def adminviewdetails(request,id):
    # complaint = Complaint.objects.filter(id=id)
    complaint = get_object_or_404(Complaint, id=id)
    # form=statusupdate()
    form = statusupdate(instance=complaint)
    if request.method == "POST":
        form = statusupdate(request.POST, instance=complaint)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user # add the user_id value to the instance
            instance.save()
            # complaint_user = complaint.user
            # complaint_user_complaint = Complaint.objects.filter(user=complaint_user, id=id).first()
            # if complaint_user_complaint:
            #     complaint_user_complaint.status = instance.status
            #     complaint_user_complaint.save()

            # complaint = Complaint.objects.get(id=complaint_id, user=complaint_user)
            # complaint.status = new_status
            # complaint.save()
            messages.success(request, 'Successfully updated')
            return redirect('admindashboard')
        else:
            messages.error(request, 'An Error occured during updating the complaint')
            return redirect('admindashboard')
    # context={'complaint':complaint, 'form': form}
    context = {'complaint': [complaint], 'form': form}

    # if request.method=='GET':
    return render(request,'admin viewdetails.html',context)
