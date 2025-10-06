import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# --- TCKN doğrulama ---

def validate_tckn(value: str):
    if not value.isdigit() or len(value) != 11:
        raise ValidationError("T.C. Kimlik No 11 haneli ve sadece rakam olmalıdır.")
    if value[0] == '0':
        raise ValidationError("T.C. Kimlik No 0 ile başlayamaz.")

class TimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Department(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Doctor(TimeStampedModel):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="doctors")
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["last_name", "first_name"]
        constraints = [
            models.UniqueConstraint(fields=["first_name", "last_name", "department"], name="uniq_doctor_in_department")
        ]

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} ({self.department.name})"

class Patient(TimeStampedModel):
    national_id = models.CharField(max_length=11, unique=True, validators=[validate_tckn], db_index=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.national_id}"

class Registration(TimeStampedModel):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Açık"
        CLOSED = "CLOSED", "Kapalı"
        CANCELLED = "CANCELLED", "İptal"

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="registrations")
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name="registrations")
    registered_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-registered_at"]
        indexes = [
            models.Index(fields=["patient", "-registered_at"], name="idx_patient_regdesc"),
        ]

    def __str__(self):
        return f"{self.patient} → {self.doctor} @ {self.registered_at:%Y-%m-%d %H:%M} ({self.status})"