from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic import View
from ACIS_system_v1.utils import render_to_pdf
from Accreditation.models import instrument_level, instrument_level_folder, user_assigned_to_folder
from django.db.models import Q


def GeneratePDF(request, pk):
    records = instrument_level_folder.objects.filter(Q(has_progress_bar=True) | Q(can_be_reviewed = True), is_deleted= False, instrument_level=pk, parent_directory= None).order_by('name') #Getting all the data inside the Program table and storing it to the context variable
    parent_folder = instrument_level.objects.select_related('instrument', 'level').get(is_deleted= False, id=pk) 
    records_count = instrument_level_folder.objects.filter(Q(has_progress_bar=True) | Q(can_be_reviewed = True), is_deleted= False, instrument_level=pk, parent_directory= None).count()#Getting all the data inside the Program table and storing it to the context variable
    template = get_template('pdf-reports/area-completion-report.html')
    total_sum=0.00
    for record in records:
        total_sum += float(record.rating)

    if total_sum:
        area_mean = float(total_sum) / float(records_count)

    else:
        area_mean = 0

    details = []
    for record in records:
        assigned_users = user_assigned_to_folder.objects.select_related('assigned_user').filter(parent_directory_id=record.id)
        details.append((record, assigned_users))

    context = {
        "records": records,
        'details': details,
        'area_mean': area_mean,
        'total_sum': total_sum,
        'parent_folder':  parent_folder
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf-reports/area-completion-report.html', context)
    return HttpResponse(pdf, content_type="application/pdf")

def CompletedArea(request, pk):
    records = instrument_level_folder.objects.filter(Q(progress_percentage=100.00) | Q(rating = 5.00), Q(has_progress_bar=True) | Q(can_be_reviewed = True), is_deleted= False, instrument_level=pk, parent_directory= None).order_by('name') #Getting all the data inside the Program table and storing it to the context variable
    parent_folder = instrument_level.objects.select_related('instrument', 'level').get(is_deleted= False, id=pk) 
    records_count = instrument_level_folder.objects.filter(Q(progress_percentage=100.00) | Q(rating = 5.00), Q(has_progress_bar=True) | Q(can_be_reviewed = True), is_deleted= False, instrument_level=pk, parent_directory= None).count()#Getting all the data inside the Program table and storing it to the context variable
    template = get_template('pdf-reports/completed-area-report.html')
    

    details = []
    for record in records:
        assigned_users = user_assigned_to_folder.objects.select_related('assigned_user').filter(parent_directory_id=record.id)
        details.append((record, assigned_users))

    context = {
        "records": records,
        'details': details,
        'parent_folder':  parent_folder,
        'records_count': records_count
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf-reports/completed-area-report.html', context)
    return HttpResponse(pdf, content_type="application/pdf")

def OngoingArea(request, pk):
    records = instrument_level_folder.objects.filter(~Q(progress_percentage=100.00), ~Q(rating=5.00), Q(has_progress_bar=True) | Q(can_be_reviewed = True), is_deleted= False, instrument_level=pk, parent_directory= None).order_by('name') #Getting all the data inside the Program table and storing it to the context variable
    parent_folder = instrument_level.objects.select_related('instrument', 'level').get(is_deleted= False, id=pk) 
    records_count = instrument_level_folder.objects.filter(~Q(progress_percentage=100.00), ~Q(rating=5.00), Q(has_progress_bar=True) | Q(can_be_reviewed = True), is_deleted= False, instrument_level=pk, parent_directory= None).count()#Getting all the data inside the Program table and storing it to the context variable
    template = get_template('pdf-reports/ongoing-area-report.html')


    details = []
    for record in records:
        assigned_users = user_assigned_to_folder.objects.select_related('assigned_user').filter(parent_directory_id=record.id)
        details.append((record, assigned_users))

    context = {
        "records": records,
        'details': details,
        'parent_folder':  parent_folder,
        'records_count': records_count

    }
    html = template.render(context)
    pdf = render_to_pdf('pdf-reports/ongoing-area-report.html', context)
    return HttpResponse(pdf, content_type="application/pdf")










def ParameterMeanReport(request, pk):
    records = instrument_level_folder.objects.filter(Q(has_progress_bar=True) | Q(can_be_reviewed = True), is_deleted= False, parent_directory=pk).order_by('name') #Getting all the data inside the Program table and storing it to the context variable
    parent_folder = instrument_level_folder.objects.select_related('instrument_level', 'parent_directory').get(is_deleted= False, id=pk) 
    template = get_template('pdf-reports/parameter-mean-report.html')
    details = []
    total_sum=0.00
    for record in records:
        total_sum += float(record.rating)

    records_count = instrument_level_folder.objects.filter(Q(has_progress_bar=True) | Q(can_be_reviewed = True), is_deleted= False, parent_directory=pk).count()#Getting all the data inside the Program table and storing it to the context variable
    if total_sum:
        area_mean = float(total_sum) / float(records_count)

    else:
        area_mean = 0
    
    for record in records:
        assigned_users = user_assigned_to_folder.objects.select_related('assigned_user').filter(parent_directory_id=record.id)
        details.append((record, assigned_users))

    context = {
        "records": records,
        'details': details,
        'parent_folder': parent_folder,
        'area_mean': area_mean,
        'total_sum': total_sum
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf-reports/parameter-mean-report.html', context)
    return HttpResponse(pdf, content_type="application/pdf")





def CompletedParameter(request, pk):
    records = instrument_level_folder.objects.filter(Q(progress_percentage=100.00) | Q(rating = 5.00), Q(has_progress_bar=True) | Q(can_be_reviewed = True), is_deleted= False, parent_directory=pk).order_by('name') #Getting all the data inside the Program table and storing it to the context variable
    parent_folder = instrument_level_folder.objects.select_related('instrument_level', 'parent_directory').get(is_deleted= False, id=pk) 
    records_count = instrument_level_folder.objects.filter(Q(progress_percentage=100.00) | Q(rating = 5.00), Q(has_progress_bar=True) | Q(can_be_reviewed = True), is_deleted= False, parent_directory=pk).count()#Getting all the data inside the Program table and storing it to the context variable
    template = get_template('pdf-reports/completed-parameter-report.html')
    

    details = []
    for record in records:
        assigned_users = user_assigned_to_folder.objects.select_related('assigned_user').filter(parent_directory_id=record.id)
        details.append((record, assigned_users))

    context = {
        "records": records,
        'details': details,
        'parent_folder':  parent_folder,
        'records_count': records_count
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf-reports/completed-parameter-report.html', context)
    return HttpResponse(pdf, content_type="application/pdf")

def OngoingParameter(request, pk):
    records = instrument_level_folder.objects.filter(~Q(progress_percentage=100.00), ~Q(rating=5.00), Q(has_progress_bar=True) | Q(can_be_reviewed = True), is_deleted= False, parent_directory_id=pk).order_by('name') #Getting all the data inside the Program table and storing it to the context variable
    parent_folder = instrument_level_folder.objects.select_related('instrument_level', 'parent_directory').get(is_deleted= False, id=pk) 
    records_count = instrument_level_folder.objects.filter(~Q(progress_percentage=100.00), ~Q(rating=5.00), Q(has_progress_bar=True) | Q(can_be_reviewed = True), is_deleted= False, parent_directory_id=pk).count()#Getting all the data inside the Program table and storing it to the context variable
    template = get_template('pdf-reports/ongoing-parameter-report.html')


    details = []
    for record in records:
        assigned_users = user_assigned_to_folder.objects.select_related('assigned_user').filter(parent_directory_id=record.id)
        details.append((record, assigned_users))

    context = {
        "records": records,
        'details': details,
        'parent_folder':  parent_folder,
        'records_count': records_count

    }
    html = template.render(context)
    pdf = render_to_pdf('pdf-reports/ongoing-parameter-report.html', context)
    return HttpResponse(pdf, content_type="application/pdf")