from django.test import TestCase
from django.contrib.auth.models import User
from .models import Complaint
from .forms import NComplaintForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.urls import reverse

# Create your tests here.
class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}

        self.user = User.objects.create_user(**self.credentials)
        self.client.login(username=self.credentials['username'], password=self.credentials['password'])
        self.response = self.client.get('/login/', follow=True)

    def test_user_authentication(self):
        self.assertTrue(self.response.context['user'].is_authenticated)
    def test_username_login(self):
        self.assertEqual(self.response.context['name'], self.credentials['username'])

class ComplaintModelTest(TestCase):
    def test_complaint_creation(self):
        complaint = Complaint.objects.create(
            complaint_title="Loud Noises at Night",
            type_complaint=Complaint.ComplaintType.NOISE_COMPLAINT,
            sent_date= timezone.now(),
            incident_date= timezone.now(),
            location_address="123 Main St",
            incident_description="There was a loud party next door."
        )
        self.assertTrue(isinstance(complaint, Complaint))
        self.assertEqual(complaint.complaint_status, Complaint.ComplaintStatus.NEW)



class NeighborComplaintFormTest(TestCase):
    # def test_valid_form(self):
    #     form_data = {
    #         'reporter_first_name': 'John',
    #         'reporter_email':'test@gmail.com',
    #         'complaint_title': 'Noise Complaint',
    #         'type_complaint': 1,
    #         'sent_date': timezone.now().strftime('%Y-%m-%d %H:%M'),
    #         'incident_date': timezone.now().strftime('%Y-%m-%d %H:%M'),
    #         'location_address': '123 Main St',
    #         'location_description':'test',
    #         'incident_description': 'Loud noise from a party.',
    #     }
    #     form = NComplaintForm(data=form_data)
    #     self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = NComplaintForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('complaint_title', form.errors) 


class ComplaintViewTest(TestCase):
    def test_neighbor_complaint_view_get(self):
        response = self.client.get(reverse('whistleblower:n-complaint'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'whistleblower/neighbor_complaint.html')

    # def test_building_complaint_view_post(self):
    #     post_data = {
    #         'reporter_first_name': 'Jane',
    #         'complaint_title': 'Maintenance Needed',
    #         'type_complaint': 4,
    #         'sent_date': timezone.now().strftime('%Y-%m-%d %H:%M'),
    #         'incident_date': timezone.now().strftime('%Y-%m-%d %H:%M'),
    #         'location_address': 'Apartment 5B',
    #         'location_description':'test',
    #         'incident_description': 'Leaking pipe in the bathroom.',
    #         'expected_completion': timezone.now().strftime('%Y-%m-%d %H:%M')
    #     }
    #     response = self.client.post(reverse('whistleblower:b-complaint'), data=post_data, follow=True)
    #     self.assertRedirects(response, '/success/')
    #     self.assertEqual(Complaint.objects.count(), 1)
        

    

       
