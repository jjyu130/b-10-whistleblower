from time import timezone

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.views import generic
from .forms import NComplaintForm
from .forms import BComplaintForm
from .models import Complaint, BuildingGroup

import os
import boto3
from botocore.exceptions import NoCredentialsError


# Tutorial used to figure out login:
# https://anmol-garg.medium.com/adding-google-oauth-2-0-to-your-django-project-the-easy-way-9df3d87d16fd

def home(request):
    if request.user.is_authenticated:
        context = {
            'name': request.user.username,
            'open_reports': Complaint.objects.filter(reporter=request.user,
                                                     complaint_status__in=[Complaint.ComplaintStatus.NEW,
                                                                           Complaint.ComplaintStatus.IN_PROGRESS]),
            'closed_reports': Complaint.objects.filter(reporter=request.user,
                                                       complaint_status=Complaint.ComplaintStatus.RESOLVED),
            'groups': BuildingGroup.objects.filter(users=request.user)
        }
        if request.user.groups.filter(name="Admin"):
            return HttpResponseRedirect('/home-admin')
        else:
            return render(request, "whistleblower/home.html", context)

    return HttpResponseRedirect('/login')


def anon_home(request):
    return render(request, "whistleblower/home_anonymous.html")


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    return render(request, "whistleblower/login.html")


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')


def neighbor_complaint(request):
    if request.method == "POST":
        form = NComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            # FName = form.cleaned_data["reporter_first_name"]
            # LName= form.cleaned_data["reporter_last_name"]
            # rPN = form.cleaned_data["reporter_phone_number"]
            # rE = form.cleaned_data["reporter_email"]
            # rD = form.cleaned_data["reporter_description"]
            # complaintTitle = form.cleaned_data["complaint_title"]
            # complaintType = form.cleaned_data["type_complaint"]
            # sDate = form.cleaned_data["sent_date"]
            # iDate = form.cleaned_data["incident_date"]
            # rName = form.cleaned_data["respondent_name"]
            # rLocation = form.cleaned_data["respondent_location"]
            # locationAdd = form.cleaned_data["location_address"]
            # locationDesc = form.cleaned_data["location_description"]
            # incidentDesc = form.cleaned_data["incident_description"]
            # addInfo = form.cleaned_data["additional_information"]
            # expecCompl = form.cleaned_data["expected_completion"]
            # complaint = Complaint.objects.create(reporter_first_name=FName, reporter_last_name=LName,
            #                                      reporter_phone_number=rPN, reporter_email=rE, reporter_description=rD, version=0,
            #                                      complaint_title=complaintTitle, type_complaint=complaintType, sent_date=sDate, incident_date=iDate,
            #                                      respondent_name=rName, respondent_location=rLocation, location_address=locationAdd,
            #                                      location_description=locationDesc, incident_description=incidentDesc,
            #                                      additional_information=addInfo,
            #                                      expected_completion=expecCompl, complaint_status=1)
            complaint = form.save()
            complaint.reporter = request.user
            complaint.save()
            return HttpResponseRedirect("/success")
    else:
        form = NComplaintForm()
    return render(request, "whistleblower/neighbor_complaint.html", {"form": form})


def building_complaint(request):
    if request.method == "POST":
        form = BComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            # FName = form.cleaned_data["reporter_first_name"]
            # LName= form.cleaned_data["reporter_last_name"]
            # rPN = form.cleaned_data["reporter_phone_number"]
            # rE = form.cleaned_data["reporter_email"]
            # rD = form.cleaned_data["reporter_description"]
            # complaintTitle = form.cleaned_data["complaint_title"]
            # complaintType = form.cleaned_data["type_complaint"]
            # sDate = form.cleaned_data["sent_date"]
            # iDate = form.cleaned_data["incident_date"]
            # rName = form.cleaned_data["respondent_name"]
            # rLocation = form.cleaned_data["respondent_location"]
            # locationAdd = form.cleaned_data["location_address"]
            # locationDesc = form.cleaned_data["location_description"]
            # incidentDesc = form.cleaned_data["incident_description"]
            # file1 = form.cleaned_data["file1"]
            # file2 = form.cleaned_data["file2"]
            # file3 = form.cleaned_data["file3"]
            # addInfo = form.cleaned_data["additional_information"]
            # expecCompl = form.cleaned_data["expected_completion"]
            # complaint = Complaint.objects.create(reporter_first_name=FName, reporter_last_name=LName,
            #                                          reporter_phone_number=rPN, reporter_email=rE, reporter_description=rD, version=0,
            #                                          complaint_title=complaintTitle, type_complaint=complaintType, sent_date=sDate, incident_date=iDate,
            #                                          respondent_name=rName, respondent_location=rLocation, location_address=locationAdd,
            #                                          location_description=locationDesc, incident_description=incidentDesc,
            #                                          file1=file1, file2=file2, file3=file3, additional_information=addInfo,
            #                                          expected_completion=expecCompl, complaint_status=1)
            form.save()
            return HttpResponseRedirect("/success")
            # else:
            #     return HttpResponseRedirect("/failure")
    else:
        form = BComplaintForm()
    return render(request, "whistleblower/building_complaint.html", {"form": form})


def success(request):
    return render(request, "whistleblower/success.html")


def failure(request):
    return render(request, "whistleblower/failure.html")


class HomeSuperAdmin(generic.ListView):
    template_name = "whistleblower/home_superadmin.html"
    context_object_name = "latest_report_list"

    def get_queryset(self):
        """"return the list of complaints (ordered by time sent)"""
        return Complaint.objects.order_by("-sent_date")


def home_admin(request):
    user = request.user
    groups = BuildingGroup.objects.filter(users=user)
    reports = Complaint.objects.all()
    return render(request, "whistleblower/home_admin.html", {"groups": groups, "reports": reports, 'name': user.username})


def get_recent_reports():
    return Complaint.objects.order_by("-sent_date")


def mark_as_resolved(request, report_id):
    complaint = get_object_or_404(Complaint, pk=report_id)
    resolution_notes = request.POST.get('resolution_notes')
    complaint.resolution_notes = resolution_notes
    complaint.complaint_status = Complaint.ComplaintStatus.RESOLVED
    complaint.save()
    return redirect('/home-admin')


class ReportView(generic.DetailView):
    model = Complaint
    context_object_name = "report"
    template_name = "whistleblower/admin_report_view.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = self.request.user.groups.filter(name="Admin")
        return context
    def dispatch(self, request, *args, **kwargs):
        report_id = self.kwargs.get('pk')
        report = get_object_or_404(Complaint, pk=report_id)
        is_admin = request.user.groups.filter(name="Admin")
        if report.complaint_status != Complaint.ComplaintStatus.IN_PROGRESS and report.complaint_status != Complaint.ComplaintStatus.RESOLVED and is_admin:
            report.complaint_status = Complaint.ComplaintStatus.IN_PROGRESS
            report.save()
        return super().dispatch(request, *args, **kwargs)



def create_building_group_page(request):
    return render(request, "whistleblower/create_building_group.html")


def create_building_group(request):
    if request.method == "POST":
        new_group = BuildingGroup(name=request.POST.get("building_name"))
        new_group.name = request.POST.get("building_name")
        new_group.save()
        new_group.users.add(request.user)
        new_group.save()
        context = {"group_id": new_group.pk}
        return render(request, "whistleblower/confirm_building_group.html", context)


def join_building_group_page(request):
    return render(request, "whistleblower/join_building_group.html")


def join_building_group(request):
    if request.method == "POST":
        building_code = request.POST.get("building_code")
        if not building_code:
            return render(request, "whistleblower/join_building_group.html", {"error_message": "Please enter a group"})
        try:
            group = BuildingGroup.objects.get(pk=building_code)
        except ObjectDoesNotExist:
            return render(request, "whistleblower/join_building_group.html", {"error_message": "Not a valid group"})
        group.users.add(request.user)
        return HttpResponseRedirect(reverse("whistleblower:home"))


def leave_building_group(request, code):
    user = request.user
    group = get_object_or_404(BuildingGroup, id=code)
    group.users.remove(user)
    return HttpResponseRedirect(reverse("whistleblower:home"))

# def did_file_upload(file):
#     if file is None:
#         return True
#     AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
#     AWS_SECRET_ACCESS = os.environ.get('AWS_SECRET_ACCESS')
#     AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
#     AWS_S3_REGION_NAME = 'us-east-1'
#     s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS,
#                       region_name=AWS_S3_REGION_NAME)
#     try:
#         s3.upload_fileobj(file, AWS_STORAGE_BUCKET_NAME, file.name)
#         return True
#     except NoCredentialsError:
#         return False
