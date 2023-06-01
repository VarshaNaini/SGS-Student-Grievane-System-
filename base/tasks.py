# tasks.py

from celery import shared_task
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.mail import send_mail
from .models import Complaint

# @shared_task(bind=True)
# def test_func(self):
#     #operations
#     for i in range(10):
#         print(i)
#     return "Done"


@shared_task
def escalate_complaint():
    try:
        pending_complaints = Complaint.objects.filter(status=3)  # Get all pending complaints

        for complaint in pending_complaints:
            # Check if the allocated time has elapsed
            if datetime.now() > complaint.allocated_time:
                # Manually escalate the complaint to the next authority based on a predefined order
                if complaint.To == 'CIVIL_HOD':
                    complaint.To = 'CEO'
                elif complaint.To == 'PRINCIPLE':
                    complaint.To = 'DIRECTOR'
                elif complaint.To == 'DIRECTOR':
                    complaint.To = 'CEO'
                else:
                    # If the complaint has reached the highest authority, mark it as escalated
                    complaint.escalated = True

                # Update the allocated time for the next authority
                complaint.allocated_time = datetime.now() + timedelta(minutes=5)

                # Save the changes to the complaint
                complaint.save()

                 # Send email to admin
                subject = 'Complaint escalated'
                message = f'Complaint ID: {complaint.id} has been escalated to you for further action.'
                from_email = 'varsha.naini@gmail.com'
                to_email = 'varsha.naini@gmail.com' # Replace with the admin's email address
                send_mail(subject, message, from_email, [to_email])

                # Send email notification to the next authority
                next_authority_email = get_authority_email(complaint.To)  # Replace with your logic to retrieve the email of the next authority
                subject = 'Complaint Escalation'
                message = f'Complaint ID: {complaint.id} has been escalated to you for further action.'
                from_email = complaint.user.email  # Replace with your email address
                to_email = next_authority_email
                send_mail(subject, message, from_email, [to_email])

                # recipient_list = [next_authority_email]
                # send_mail(subject, message, from_email, recipient_list)

    except Complaint.DoesNotExist:
        # Handle the case where the complaint is not found
        pass

def get_authority_email(authority):
    # Define a dictionary mapping authority names to their respective email addresses
    authority_emails = {
        'CIVIL_HOD': 'varsha.naini@gmail.com',
        'CSE_HOD': 'revathi.naini@gmail.com',
        'ECE_HOD': 'ecehod@example.com',
        'ECM_HOD': 'ecmhod@example.com',
        'EEE_HOD': 'eeehod@example.com',
        'IT_HOD': 'ithod@example.com',
        'MECH_HOD': 'mechhod@example.com',
        'MBA_HOD': 'mbahod@example.com',
        'MANAGEMENT': 'management@example.com',
        'PRINCIPLE': 'principal@example.com',
        'DIRECTOR': 'director@example.com',
        'CEO': 'varsha.naini@gmail.com'
    }
    
    return authority_emails.get(authority, 'default@example.com')  # Replace 'default@example.com' with your default email address



# @shared_task
# def escalate_complaint(complaint_id):
#     try:
#         complaint = Complaint.objects.get(id=complaint_id)

#         if complaint.status != 3:  # Check if the complaint is still pending
#             return

#         # Check if the allocated time has elapsed
#         if datetime.now() > complaint.allocated_time:
#             # Manually escalate the complaint to the next authority based on a predefined order
#             if complaint.To == 'CIVIL_HOD':
#                 complaint.To = 'PRINCIPLE'
#             elif complaint.To == 'PRINCIPLE':
#                 complaint.To = 'DIRECTOR'
#             elif complaint.To == 'DIRECTOR':
#                 complaint.To = 'CEO'
#             else:
#                 # If the complaint has reached the highest authority, mark it as escalated
#                 complaint.escalated = True

#             # Update the allocated time for the next authority
#             complaint.allocated_time = datetime.now() + timedelta(hours=24)

#             # Save the changes to the complaint
#             complaint.save()

#             # Send email notification to the next authority
#             next_authority_email = get_authority_email(complaint.To)  # Replace with your logic to retrieve the email of the next authority
#             subject = 'Complaint Escalation'
#             message = f'Complaint ID: {complaint.id} has been escalated to you for further action.'
#             from_email = complaint.user.email  # Replace with your email address
#             to_email = next_authority_email
#             send_mail(subject, message, from_email, [to_email])

#             # recipient_list = [next_authority_email]
#             # send_mail(subject, message, from_email, recipient_list)

#     except Complaint.DoesNotExist:
#         # Handle the case where the complaint is not found
#         pass

# def get_authority_email(authority):
#     # Define a dictionary mapping authority names to their respective email addresses
#     authority_emails = {
#         'CIVIL_HOD': 'varsha.naini@gmail.com',
#         'CSE_HOD': 'revathi.naini@gmail.com',
#         'ECE_HOD': 'ecehod@example.com',
#         'ECM_HOD': 'ecmhod@example.com',
#         'EEE_HOD': 'eeehod@example.com',
#         'IT_HOD': 'ithod@example.com',
#         'MECH_HOD': 'mechhod@example.com',
#         'MBA_HOD': 'mbahod@example.com',
#         'MANAGEMENT': 'management@example.com',
#         'PRINCIPLE': 'principal@example.com',
#         'DIRECTOR': 'director@example.com',
#         'CEO': 'ntr.naini@gmail.com'
#     }

    # Retrieve the email of the next authority based on the authority name
    # return authority_emails.get(authority, 'admin@example.com')  # Return the admin's email as default


# @shared_task
# def check_complaint_status():
#     complaints = Complaint.objects.filter(status=3)
#     for complaint in complaints:
#         if timezone.now() > complaint.deadline:
#             # escalate the complaint to the next higher authority
#             complaint.status = 'escalated'
#             complaint.authority = get_next_authority(complaint.authority)
#             complaint.deadline = get_deadline_for_authority(complaint.authority)
            # complaint.save()
