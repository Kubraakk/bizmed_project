from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import Department, Doctor, Patient, Registration
from .serializers import DepartmentSerializer, DoctorSerializer, PatientSerializer, RegistrationSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.select_related("department").all()
    serializer_class = DoctorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["first_name", "last_name", "department__name"]
    ordering_fields = ["last_name", "first_name"]

    def get_queryset(self):
        qs = super().get_queryset()
        dept = self.request.query_params.get("department")
        if dept:
            qs = qs.filter(department_id=dept)
        return qs

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["first_name", "last_name", "national_id"]

    def get_queryset(self):
        qs = super().get_queryset()
        nid = self.request.query_params.get("national_id")
        if nid:
            qs = qs.filter(national_id=nid)
        return qs

    @action(detail=True, methods=["get"])
    def registrations(self, request, pk=None):
        patient = self.get_object()
        regs = Registration.objects.select_related("doctor", "patient").filter(patient=patient)
        data = RegistrationSerializer(regs, many=True).data
        return Response(data)

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.select_related("patient", "doctor").all()
    serializer_class = RegistrationSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        patient = self.request.query_params.get("patient")
        doctor = self.request.query_params.get("doctor")
        if patient:
            qs = qs.filter(patient_id=patient)
        if doctor:
            qs = qs.filter(doctor_id=doctor)
        return qs