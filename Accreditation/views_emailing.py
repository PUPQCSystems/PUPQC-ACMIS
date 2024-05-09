from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import render, redirect

def email_when_folder_approved(folder, user, remarks):
    email_subject = "Folder Approved"
    user_email = user.assigned_user.email
    template = render_to_string('email-templates/email-when-approved.html', 
                                            {   'user': user
                                                , 'remarks': remarks
                                                , 'folder': folder
                                                })
    
    email = EmailMessage(
        email_subject,
        template,
        settings.EMAIL_HOST_USER,
        [user_email],
    )

    email.content_subtype = "html"
    email.fail_silently=False
    # Send the email
    email.send()
 

def email_when_folder_request_resubmission(folder, user, remarks):
    email_subject = "Folder Requires Resubmission"
    user_email = user.assigned_user.email
    template = render_to_string('email-templates/email-when-request-resubmission.html', 
                                                {   'user': user
                                                , 'remarks': remarks
                                                , 'folder': folder
                                                })
    
    email = EmailMessage(
        email_subject,
        template,
        settings.EMAIL_HOST_USER,
        [user_email],
    )

    email.content_subtype = "html"
    email.fail_silently=False
    # Send the email
    email.send()


def email_when_folder_for_review(folder, user, remarks):
    email_subject = "Folder is Under Review"
    user_email = user.assigned_user.email
    template = render_to_string('email-templates/email-when-for-review.html', 
                                            {   'user': user
                                                , 'remarks': remarks
                                                , 'folder': folder
                                                })
    
    email = EmailMessage(
        email_subject,
        template,
        settings.EMAIL_HOST_USER,
        [user_email],
    )

    email.content_subtype = "html"
    email.fail_silently=False
    # Send the email
    email.send()


def email_when_file_approved(file, user, remarks):
    email_subject = "File Approved"
    user_email = user.assigned_user.email
    template = render_to_string('email-templates/email-when-file-approved.html', 
                                            {   'user': user
                                                , 'remarks': remarks
                                                , 'file': file
                                                })
    
    email = EmailMessage(
        email_subject,
        template,
        settings.EMAIL_HOST_USER,
        [user_email],
    )

    email.content_subtype = "html"
    email.fail_silently=False
    # Send the email
    email.send()
 

def email_when_file_request_resubmission(file, user, remarks):
    email_subject = "File Requires Resubmission"
    user_email = user.assigned_user.email
    template = render_to_string('email-templates/email-when-file-request-resubmission.html', 
                                                {   'user': user
                                                , 'remarks': remarks
                                                , 'file': file
                                                })
    
    email = EmailMessage(
        email_subject,
        template,
        settings.EMAIL_HOST_USER,
        [user_email],
    )

    email.content_subtype = "html"
    email.fail_silently=False
    # Send the email
    email.send()


def email_when_file_for_review(file, user, remarks):
    email_subject = "File is Under Review"
    user_email = user.assigned_user.email
    template = render_to_string('email-templates/email-when-file-for-review.html', 
                                            {   'user': user
                                                , 'remarks': remarks
                                                , 'file': file
                                                })
    
    email = EmailMessage(
        email_subject,
        template,
        settings.EMAIL_HOST_USER,
        [user_email],
    )

    email.content_subtype = "html"
    email.fail_silently=False
    # Send the email
    email.send()