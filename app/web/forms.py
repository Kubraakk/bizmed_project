from django import forms
from core.models import Patient, Registration, Doctor, Department

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["national_id", "first_name", "last_name", "phone", "address"]

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ["department", "doctor", "notes"]

    department = forms.ModelChoiceField(queryset=Department.objects.all(), label="Bölüm")
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.none(), label="Doktor")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "department" in self.data:
            try:
                dep_id = int(self.data.get("department"))
                self.fields["doctor"].queryset = Doctor.objects.filter(department_id=dep_id)
            except (ValueError, TypeError):
                pass


class TCKNSearchForm(forms.Form):
    national_id = forms.CharField(max_length=11, label="T.C. Kimlik No")