from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from core.models import Patient, Registration,Doctor, Department
from .forms import PatientForm, RegistrationForm, TCKNSearchForm
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.contrib import messages




class HomeView(TemplateView):
    template_name = "web/home.html"

    def get(self, request, *args, **kwargs):
        list(messages.get_messages(request))
        return super().get(request, *args, **kwargs)



class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientForm
    template_name = "web/patient_create.html"

    def form_valid(self, form):
        national_id = form.cleaned_data.get("national_id")
        existing = Patient.objects.filter(national_id=national_id).first()

        if existing:
            if (
                existing.first_name != form.cleaned_data["first_name"]
                or existing.last_name != form.cleaned_data["last_name"]
            ):
                messages.error(self.request, "❌ Bu T.C. zaten başka bir isimle kayıtlı!")
                return self.render_to_response(self.get_context_data(form=form))

            messages.info(self.request, "ℹ️ Bu hasta zaten sistemde kayıtlı, kayıt sayfasına yönlendiriliyorsunuz...")
            self.request.session["selected_patient_id"] = str(existing.id)
            context = self.get_context_data(form=form)
            context["redirect_url"] = reverse("registration-create")
            return self.render_to_response(context)

        patient = form.save()
        self.request.session["selected_patient_id"] = str(patient.id)
        messages.success(self.request, "✅ Yeni hasta kaydı oluşturuldu, yönlendiriliyorsunuz...")
        context = self.get_context_data(form=form)
        context["redirect_url"] = reverse("registration-create")

        return self.render_to_response(context)



class RegistrationCreateView(CreateView):
    model = Registration
    form_class = RegistrationForm
    template_name = "web/registration_create.html"


    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("selected_patient_id"):
            messages.warning(request, "Önce hasta ekleyin ya da seçin.")
            return redirect(reverse("patient-create"))
        return super().dispatch(request, *args, **kwargs)
    def get_initial(self):
        initial = super().get_initial()
        patient_id = self.request.session.get("selected_patient_id")
        if patient_id:
            initial["patient"] = Patient.objects.get(id=patient_id)

        dep_id = self.request.GET.get("department")
        if dep_id:
            initial["department"] = dep_id

        return initial


    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        dep_id = self.request.GET.get("department")

        if dep_id:
            form.fields["doctor"].queryset = Doctor.objects.filter(department_id=dep_id)
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
        self.request.session.pop("selected_patient_id", None)
        messages.success(self.request, "Kayıt başarıyla oluşturuldu.")
        return redirect(reverse("home"))

class TCKNSearchView(View):
    def get(self, request):
        return render(request, "web/tckn_search.html")

class DefinitionView(View):
    def get(self, request):
        departments = Department.objects.all()
        doctors = Doctor.objects.select_related("department").all()
        return render(request, "web/definitions.html", {
            "departments": departments,
            "doctors": doctors,
        })

    def post(self, request):
        if "add_department" in request.POST:
            name = request.POST.get("department_name")
            if name:
                Department.objects.get_or_create(name=name)
        elif "add_doctor" in request.POST:
            first = request.POST.get("first_name")
            last = request.POST.get("last_name")
            dept_id = request.POST.get("department_id")
            if first and last and dept_id:
                Doctor.objects.create(
                    first_name=first,
                    last_name=last,
                    department_id=dept_id
                )
        elif "delete_department_id" in request.POST:
            dep_id = request.POST.get("delete_department_id")
            Department.objects.filter(id=dep_id).delete()
        elif "delete_doctor_id" in request.POST:
            doc_id = request.POST.get("delete_doctor_id")
            Doctor.objects.filter(id=doc_id).delete()

        return redirect("definitions")
