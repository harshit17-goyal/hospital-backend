from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Patient, MedicalRecord

class APITests(APITestCase):

    def setUp(self):
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.patients_url = reverse('patients')
        self.record_add_url = reverse('add_record')

        # Create users
        self.doctor1 = User.objects.create_user(username='doc1', password='testpass123', role='doctor')
        self.doctor2 = User.objects.create_user(username='doc2', password='testpass456', role='doctor')

        # Login doctor1
        response = self.client.post(self.login_url, {'username': 'doc1', 'password': 'testpass123'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_signup(self):
        data = {'username': 'newdoc', 'password': 'pass1234', 'email': 'new@doc.com', 'role': 'doctor'}
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username='newdoc').exists(), True)

    def test_patient_creation(self):
        data = {'name': 'John Doe', 'age': 30, 'gender': 'Male', 'address': '123 Street'}
        response = self.client.post(self.patients_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patient.objects.count(), 1)

    def test_view_own_patients_only(self):
        # Doctor1 creates a patient
        self.client.post(self.patients_url, {'name': 'Jane', 'age': 28, 'gender': 'Female', 'address': 'ABC Road'})
        
        # Doctor2 logs in
        response = self.client.post(self.login_url, {'username': 'doc2', 'password': 'testpass456'})
        token2 = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token2)

        # Doctor2 should not see doctor1's patients
        response = self.client.get(self.patients_url)
        self.assertEqual(len(response.data), 0)

    def test_prevent_access_to_others_records(self):
        # Doctor1 creates a patient and a record
        response = self.client.post(self.patients_url, {'name': 'Tom', 'age': 35, 'gender': 'Male', 'address': 'XYZ'})
        patient_id = response.data['id']

        self.client.post(self.record_add_url, {
            'patient': patient_id,
            'symptoms': 'Fever',
            'diagnosis': 'Flu',
            'treatment': 'Rest and hydration'
        })

        # Doctor2 logs in
        response = self.client.post(self.login_url, {'username': 'doc2', 'password': 'testpass456'})
        token2 = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token2)

        # Try accessing doctor1’s patient records
        record_url = reverse('patient_records', args=[patient_id])
        response = self.client.get(record_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
