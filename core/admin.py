from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import Patient, MedicalRecord


admin.site.register(User, UserAdmin)
admin.site.register(Patient)
admin.site.register(MedicalRecord)
