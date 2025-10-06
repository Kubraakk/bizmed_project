from django.urls import path
from .views import HomeView,PatientCreateView, RegistrationCreateView, TCKNSearchView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('patients/new/', PatientCreateView.as_view(), name='patient-create'),
    path('registrations/new/', RegistrationCreateView.as_view(), name='registration-create'),
    path('search/tckn/', TCKNSearchView.as_view(), name='tckn-search'),
]