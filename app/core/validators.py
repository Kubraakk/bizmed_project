from django.core.exceptions import ValidationError
from django.utils.timezone import localdate
#from .models import Registration
import re

def validate_tckn(value: str):
    if not value.isdigit() or len(value) != 11:
        raise ValidationError("T.C. Kimlik No 11 haneli ve sadece rakam olmalıdır.")
    if value[0] == '0':
        raise ValidationError("T.C. Kimlik No 0 ile başlayamaz.")

import re
from django.core.exceptions import ValidationError

def validate_phone(value):
    if not value:
        return value  # boş olabilir

    # Rakam dışı her şeyi kaldır (boşluk, tire vs temizler)
    cleaned = re.sub(r"[^\d]", "", value)

    # +90 ile başlayanları düzelt
    if cleaned.startswith("90") and len(cleaned) == 12:
        cleaned = cleaned[2:]

    # Başında 0 yoksa ekle
    if len(cleaned) == 10 and cleaned.startswith("5"):
        cleaned = "0" + cleaned

    # Final kontrol: 11 haneli olmalı ve 05 ile başlamalı
    if not (len(cleaned) == 11 and cleaned.startswith("05")):
        raise ValidationError("Telefon numarası 05XXXXXXXXX formatında olmalıdır.")

    # Otomatik formatlama: 0555 123 45 67
    formatted = f"{cleaned[:4]} {cleaned[4:7]} {cleaned[7:9]} {cleaned[9:11]}"

    return formatted

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