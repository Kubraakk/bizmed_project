from rest_framework import serializers
from core.models import Department, Doctor, Patient, Registration

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

class DoctorSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = Doctor
        fields = ["id", "first_name", "last_name", "department", "department_name", "phone", "is_active", "created_at", "updated_at"]

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["id", "national_id", "first_name", "last_name", "phone", "address", "created_at", "updated_at"]

class RegistrationSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.__str__", read_only=True)
    doctor_name = serializers.CharField(source="doctor.__str__", read_only=True)

    class Meta:
        model = Registration
        fields = ["id", "patient", "patient_name", "doctor", "doctor_name", "registered_at", "status", "notes", "created_at", "updated_at"]