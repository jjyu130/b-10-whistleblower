from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


# Create your models here.
class BuildingGroup(models.Model):
    name = models.CharField(max_length=50, null=False)
    User = get_user_model()
    users = models.ManyToManyField(User, null=True)


class Complaint(models.Model):
    class ComplaintType(models.IntegerChoices):
        NOISE_COMPLAINT = 1, "Noise Complaint"
        MESSINESS = 2, "Messiness"
        STOLEN_ITEM = 3, "Stolen Item"
        MAINTENANCE = 4, "Maintenance"
        PROPERTY_DAMAGE = 5, "Property Damage"
        PARKING_LOT = 6, "Parking Lot"
        LOITERING = 7, "Loitering"
        OTHER = 8, "Other"

    class ComplaintStatus(models.IntegerChoices):
        NEW = 1, "New"
        IN_PROGRESS = 2, "In Progress"
        RESOLVED = 3, "Resolved"

    # All Personal Information is Optional
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    resolution_notes = models.TextField(max_length=500, null=True, blank=True)
    reporter_first_name = models.CharField(max_length=50, null=True, blank=True)
    reporter_last_name = models.CharField(max_length=50, null=True, blank=True)
    reporter_phone_number = models.CharField(max_length=12, null=True, blank=True)
    reporter_email = models.CharField(max_length=50, null=True, blank=True)
    reporter_description = models.TextField(max_length=400, null=True, blank=True)
    # All Personal Information is Optional

    version = models.IntegerField(default=0)
    complaint_title = models.CharField(max_length=200)
    type_complaint = models.PositiveSmallIntegerField(
        choices=ComplaintType.choices, default=ComplaintType.NOISE_COMPLAINT)
    sent_date = models.DateTimeField("Date Sent")
    incident_date = models.DateTimeField("Date of Incident")
    respondent_name = models.CharField(max_length=50, null=True, blank= True)
    respondent_location = models.TextField(max_length=200, null=True, blank=True)
    location_address = models.CharField(max_length=50,)
    location_description = models.TextField(max_length=500)
    incident_description = models.TextField(max_length=500)
    # Need to work out how to upload and connect file upload
    file1 = models.FileField(upload_to="report_files", null=True, blank=True)
    file2 = models.FileField(upload_to="report_files", null=True, blank=True)
    file3 = models.FileField(upload_to="report_files", null=True, blank=True)
    additional_information = models.TextField(max_length=500, null=True, blank=True)
    expected_completion = models.DateTimeField("Expected time completed", null=True)
    complaint_status = models.PositiveSmallIntegerField(
        choices=ComplaintStatus.choices, default=ComplaintStatus.NEW)
    group = models.ForeignKey(BuildingGroup, on_delete=models.CASCADE, null=True)
    def complaint_status_phrase(self):
        status_mapping = {
            self.ComplaintStatus.NEW: "New",
            self.ComplaintStatus.IN_PROGRESS: "In Progress",
            self.ComplaintStatus.RESOLVED: "Resolved"
        }
        return status_mapping.get(self.complaint_status, "Unknown")

