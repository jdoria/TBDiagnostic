from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.patient.views import index, PatientRead, PatientCreate, PatientList, PatientUpdate, PatientDelete, \
    listado, buscar_codigos, PatientDiagnostic, export_patient, GeneratePDF, upload_csv, PatientValidar

app_name = 'patient'

urlpatterns = [
    path('', login_required(index), name='index'),
    path('crear', login_required(PatientCreate.as_view()), name='patient_crear'),
    path('lista', login_required(PatientList.as_view()), name='patient_lista'),
    url(r'^leer/(?P<pk>\d+)/$', login_required(PatientRead.as_view()), name='patient_leer'),
    url(r'^editar/(?P<pk>\d+)/$', login_required(PatientUpdate.as_view()), name='patient_editar'),
    url(r'^eliminar/(?P<pk>\d+)/$', login_required(PatientDelete.as_view()), name='patient_eliminar'),
    path('listado', login_required(listado), name='listado'),
    path('buscar', login_required(buscar_codigos), name='buscador'),
    url(r'^diagnosticar/(?P<pk>\d+)/$', login_required(PatientDiagnostic.as_view()), name='patient_diagnosticar'),
    url(r'^validar/(?P<pk>\d+)/$', login_required(PatientValidar), name='patient_validar'),
    path('cargar', login_required(upload_csv), name='patient_upload'),
    path('exportar', login_required(export_patient), name='patient_export'),
    path('exportar_pdf', login_required(GeneratePDF.as_view()), name='patient_export_pdf'),
]
