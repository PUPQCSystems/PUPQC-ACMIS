import requests
from rest_framework import generics, serializers
from Accreditation.models import program_accreditation
from Users.models import category_training, faculty_certificates, seminar_workshop_training
from .serializers import CategorySerializer, FacultyCertificateSerializer, WorkshopsSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import QueryDict


@login_required
def landing_page(request, program_accred_pk):
    return render(request,'exhibit-page/landing-page.html', {'program_accred_pk':program_accred_pk})
