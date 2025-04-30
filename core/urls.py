from django.urls import path
from .views import (
    SignupView, LoginView, PatientCreateListView,
    AddMedicalRecordView, PatientRecordsView
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('patients/', PatientCreateListView.as_view(), name='patients'),
    path('patients/records/add', AddMedicalRecordView.as_view(), name='add_record'),
    path('patients/<int:pk>/records/', PatientRecordsView.as_view(), name='patient_records'),
]
