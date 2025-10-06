from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from core.models import Patient, Registration,Doctor
from .forms import PatientForm, RegistrationForm, TCKNSearchForm
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.contrib import messages




class HomeView(TemplateView):
    template_name = "web/home.html"


class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientForm
    template_name = "web/patient_create.html"

    def form_valid(self, form):
        patient = form.save()
        self.request.session["selected_patient_id"] = str(patient.id)
        return redirect(reverse("registration-create"))

class RegistrationCreateView(CreateView):
    model = Registration
    form_class = RegistrationForm
    template_name = "web/registration_create.html"

    def dispatch(self, request, *args, **kwargs):
        # Hasta seçilmeden bu sayfaya gelindiyse yönlendir
        if not request.session.get("selected_patient_id"):
            messages.warning(request, "Önce hasta ekleyin ya da seçin.")
            return redirect(reverse("patient-create"))
        return super().dispatch(request, *args, **kwargs)
    def get_initial(self):
        initial = super().get_initial()

        # Seçili hastayı koruyorsun:
        patient_id = self.request.session.get("selected_patient_id")
        if patient_id:
            initial["patient"] = Patient.objects.get(id=patient_id)

        # 🔧 GET ile gelen department değerini select'e geri yaz
        dep_id = self.request.GET.get("department")
        if dep_id:
            initial["department"] = dep_id   # pk string vermek yeterli

        return initial


    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        dep_id = self.request.GET.get("department")

        # Dinamik doktor filtreleme
        if dep_id:
            form.fields["doctor"].queryset = Doctor.objects.filter(department_id=dep_id)
            # 🔧 select'in ekranda seçili görünmesi için:
            form.fields["department"].initial = dep_id
        else:
            form.fields["doctor"].queryset = Doctor.objects.none()

        return form

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        pid = self.request.session.get("selected_patient_id")
        ctx["patient"] = Patient.objects.filter(id=pid).first()

        form = ctx.get("form")
        if form:
            ctx["doctors"] = form.fields["doctor"].queryset
            ctx["selected_doctor_id"] = (form["doctor"].value() or None)
        return ctx

    def form_valid(self, form):
        patient_id = self.request.session.get("selected_patient_id")
        if patient_id:
            form.instance.patient_id = patient_id
        # İşlem tamam: session temizle
        self.request.session.pop("selected_patient_id", None)
        messages.success(self.request, "Kayıt başarıyla oluşturuldu.")
        return super().form_valid(form)

class TCKNSearchView(View):
    def get(self, request):
        form = TCKNSearchForm()
        return render(request, 'web/tckn_search.html', {"form": form})
    def post(self, request):
        form = TCKNSearchForm(request.POST)
        context = {"form": form, "patient": None, "registrations": []}
        if form.is_valid():
            nid = form.cleaned_data["national_id"]
            patient = Patient.objects.filter(national_id=nid).first()
            context["patient"] = patient
            if patient:
                context["registrations"] = Registration.objects.select_related("doctor").filter(patient=patient)
        return render(request, 'web/tckn_search.html', context)