from django.core.exceptions import ValidationError
from django.utils.timezone import localdate
#from .models import Registration
import re

def validate_tckn(value: str):
    if not value.isdigit() or len(value) != 11:
        raise ValidationError("T.C. Kimlik No 11 haneli ve sadece rakam olmalıdır.")
    if value[0] == '0':
        raise ValidationError("T.C. Kimlik No 0 ile başlayamaz.")

def validate_phone(value):
    phone_regex = r"^\+?\d{10,15}$"
    if value and not re.match(phone_regex, value):
        raise ValidationError("Telefon numarası geçerli bir formatta değil.")
"""
def validate_unique_daily_registration(patient, doctor):
    today = localdate()
    exists = Registration.objects.filter(
        patient=patient,
        doctor=doctor,
        registered_at__date=today
    ).exists()

    if exists:
        raise ValidationError("Bu hasta için bugün aynı doktora zaten kayıt açılmış.")
"""