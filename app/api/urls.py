from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, DoctorViewSet, PatientViewSet, RegistrationViewSet

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'registrations', RegistrationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]