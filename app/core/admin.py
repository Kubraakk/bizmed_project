from django.contrib import admin
from .models import Department, Doctor, Patient, Registration

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "department", "is_active")
    list_filter = ("department", "is_active")
    search_fields = ("first_name", "last_name", "phone")

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "national_id", "phone")
    search_fields = ("first_name", "last_name", "national_id", "phone")

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "registered_at", "status")
    list_filter = ("status", "doctor__department")
    search_fields = ("patient__first_name", "patient__last_name", "patient__national_id", "doctor__last_name")