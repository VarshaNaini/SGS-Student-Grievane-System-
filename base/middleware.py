# from datetime import datetime
# from django.utils.deprecation import MiddlewareMixin
# from datetime import timedelta


# class ComplaintEscalationMiddleware(MiddlewareMixin):

#     def process_request(self, request):
#         # Check if the request is for a complaint submission or update
#         if request.path.startswith('/compStatusP/') or request.path.startswith('/compStatusS/') or request.path.startswith('/compStatusIP/') or request.path.startswith('/compStatusA/'):
#             # Get the complaint object
#             complaint = self.get_complaint_object(request)

#             # Check if the complaint is unresolved and has exceeded its allocated time
#             if complaint.status == 'Pending' and datetime.now() > complaint.allocated_time:
#                 # Escalate the complaint to the next higher authority
#                 self.escalate_complaint(complaint)

#     def get_complaint_object(request):
#         complaint_id = request.path.split('/')[-2]
#         complaint = Complaint.objects.get(id=complaint_id)
#         return complaint
    
#     def escalate_complaint(complaint):
#         # if complaint.responsible_person == 'HOD':
#         if complaint.To.endswith('_HOD'):
#             complaint.To = 'Principal'
#             complaint.allocated_time = datetime.now() + timedelta(hours=1)
#         elif complaint.To == 'Principal':
#             complaint.To = 'Director'
#             complaint.allocated_time = datetime.now() + timedelta(hours=1)
#         else:
#             complaint.To = 'CEO'
#             complaint.allocated_time = datetime.now() + timedelta(hours=1)

#         complaint.status = 'Pending'
#         complaint.save()






from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from .models import Complaint


class ComplaintEscalationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is for a complaint submission or update
        if request.path.startswith('/compStatusP/') or request.path.startswith('/compStatusS/') or request.path.startswith('/compStatusIP/') or request.path.startswith('/compStatusA/'):
            # Get the complaint object
            complaint = self.get_complaint_object(request)

            # Check if the complaint is unresolved and has exceeded its allocated time
            if complaint.status == 'Pending' and datetime.now() > complaint.allocated_time:
                # Escalate the complaint to the next higher authority
                self.escalate_complaint(complaint)


                if request.path.startswith('/compStatusP/') or request.path.startswith('/compStatusS/') or request.path.startswith('/compStatusIP/') or request.path.startswith('/compStatusA/'):
                    complaint_id = request.path.split('/')[-2]
                    complaint = self.get_complaint_object(complaint_id)

                    if complaint and complaint.status == 'Pending' and datetime.now() > complaint.allocated_time:
                        self.escalate_complaint(complaint)

        response = self.get_response(request)

        return response
    

    

    def get_complaint_object(self, complaint_id):
        try:
            complaint = Complaint.objects.get(id=complaint_id)
            return complaint
        except Complaint.DoesNotExist:
            return None


    def escalate_complaint(self, complaint):
        # if complaint.responsible_person == 'HOD':
        if complaint.To.endswith('_HOD'):
            complaint.To = 'Principal'
            complaint.allocated_time = datetime.now() + timedelta(hours=1)
        elif complaint.To == 'Principal':
            complaint.To = 'Director'
            complaint.allocated_time = datetime.now() + timedelta(hours=1)
        else:
            complaint.To = 'CEO'
            complaint.allocated_time = datetime.now() + timedelta(hours=1)

        complaint.status = 'Pending'
        complaint.current_handler = None
        complaint.save()

        # Send email notification to the new responsible person
        recipient_email = f'{complaint.To.lower()}@example.com'
        subject = 'Complaint Escalated'
        message = f'Hello,\n\nYou have been assigned a new complaint. Please go to {settings.BASE_URL}{reverse("complaint_detail", args=[complaint.id])} to view the details.\n\nThanks,\nThe Complaint System Team'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email], fail_silently=False)

