from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from apps.patient.forms import PatientForm
from apps.patient.models import Patient
from django.urls import reverse_lazy, reverse
from modelo import modelo
from django.contrib import messages
import json, csv, codecs
import openpyxl
from apps.patient.resources import PatientResource
from TBDiagnostic.utilpdf import render_pdf


# Create your views here.


# App index
def index(request):
    return render(request, 'patient/index.html')


# Search
def buscar_codigos(request):
    c = request.GET['busqueda']
    patients = Patient.objects.filter(codigo__icontains=c)

    patients = [{'id': patient.id,
                 'codigo': patient.codigo,
                 'edad': patient.edad,
                 'sexo': patient.sexo,
                 'vih': patient.vih,
                 'info_clinica': patient.info_clinica,
                 'hab_calle': patient.hab_calle,
                 'diabetes': patient.diabetes} for patient in patients]

    return HttpResponse(json.dumps(patients), content_type='application/json')


def listado(request):
    lista = serializers.serialize('json', Patient.objects.all())
    return HttpResponse(lista, content_type='application/json')


# Read only view
class PatientRead(DetailView):
    model = Patient
    template_name = 'patient/patient_read.html'


# Creation View
class PatientCreate(CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patient/patient_form.html'
    success_url = reverse_lazy('patient:index')


# List View
class PatientList(ListView):
    model = Patient
    template_name = 'patient/patient_list.html'
    paginate_by = 5

    def get_queryset(self):
        return Patient.objects.order_by('codigo')


# Update View
class PatientUpdate(UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = "patient/patient_update.html"
    success_url = reverse_lazy('patient:patient_lista')


# Delete View
class PatientDelete(DeleteView):
    model = Patient
    template_name = 'patient/patient_delete.html'
    success_url = reverse_lazy('patient:patient_lista')


# Diagnostic View
class PatientDiagnostic(DeleteView):
    model = Patient

    def get(self, request, pk):
        patient = Patient.objects.get(id=pk)
        sexo = 0
        edad = 0
        clinico = 0
        sida = 0
        h_calle = 0
        diabetes = 0

        if patient.sexo == True:
            sexo = 1
        elif patient.sexo == False:
            sexo = -1
        else:
            sexo = 0

        if patient.info_clinica == True:
            clinico = 1
        elif patient.info_clinica == False:
            clinico = -1
        else:
            clinico = 0

        if patient.vih == True:
            sida = 1
        elif patient.vih == False:
            sida = -1
        else:
            sida = 0

        if patient.hab_calle == True:
            h_calle = 1
        elif patient.hab_calle == False:
            h_calle = -1
        else:
            h_calle = 0

        if patient.diabetes == True:
            diabetes = 1
        elif patient.diabetes == False:
            diabetes = -1
        else:
            diabetes = 0

        x = modelo.modelo(sexo, edad / 80, clinico, sida, h_calle, diabetes);
        z = x.diagnosticar();
        mlp = z["mlp"]
        som = z["som"]
        context = {'patient': patient, 'mlp': mlp, 'som': som}
        return render(request, 'patient/patient_diagnostic.html', context)

    # template_name = 'patient/patient_diagnostic.html'


# Validation View
class PatientValidate(UpdateView):
    model = Patient
    # form_class = PatientForm
    fields = ['validacion']
    template_name = "patient/patient_validar.html"
    success_url = reverse_lazy('patient:patient_lista')

# Validation View
def PatientValidar(request, pk):
    patient = Patient.objects.get(id=pk)
    if request.method == "POST":
        var = request.POST['val']
        print("VAR: ", var)
        if var == "SI":
            var = True
        else:
            var = False
        patient.validacion = var
        patient.save()
        return HttpResponseRedirect(reverse('patient:patient_lista'))
    else:
        return render(request, 'patient/patient_validar.html', {'patient':patient})
    #return render(request, 'patient/patient_validar.html', {'patient': patient})



# Export to xls view
def export_patient(request):
    patient_resource = PatientResource()
    print(type(patient_resource.Meta.model.sexo))
    dataset = patient_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="patients.xls"'
    return response


# Export to pdf view
class GeneratePDF(ListView):

    def get(self, request, *args, **kwargs):
        patients = Patient.objects.all().order_by('pk')
        pdf = render_pdf("patient/patient_pdf.html", {'data': patients})
        return HttpResponse(pdf, content_type="application/pdf")


# Bulk upload view
def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "patient/patient_upload.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'El archivo cargado no es .csv')
            return HttpResponseRedirect(reverse("patient:patient_upload"))
        # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "El archivo cargado es demasiado grande (%.2f MB)." % (csv_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("patient:patient_upload"))

        file_data = csv_file.read().decode('utf-8')

        lines = file_data.split("\n")
        aux = 0
        # loop over the lines and save them in db. If error , store as string and then display
        for line in lines:
            if line == "":
                pass
            else:
                fields = line.split(";")
                data_dict = {}
                data_dict["codigo"] = fields[0]
                data_dict["edad"] = fields[1]

                if fields[2] == "Masculino" or fields[2] == "masculino":
                    data_dict["sexo"] = True
                elif fields[2] == "Femenino" or fields[2] == "femenino":
                    data_dict["sexo"] = False
                else:
                    data_dict["sexo"] = None

                if fields[3] == "Sí" or fields[3] == "Si" or fields[3] == "sí" or fields[3] == "si":
                    data_dict["vih"] = True
                elif fields[3] == "No" or fields[3] == "no":
                    data_dict["vih"] = False
                else:
                    data_dict["vih"] = None

                if fields[4] == "Sí" or fields[4] == "Si" or fields[4] == "sí" or fields[4] == "si":
                    data_dict["diabetes"] = True
                elif fields[4] == "No" or fields[4] == "no":
                    data_dict["diabetes"] = False
                else:
                    data_dict["diabetes"] = None

                if fields[5] == "Sí" or fields[5] == "Si" or fields[5] == "sí" or fields[5] == "si":
                    data_dict["hab_calle"] = True
                elif fields[5] == "No" or fields[5] == "no":
                    data_dict["hab_calle"] = False
                else:
                    data_dict["hab_calle"] = None

                if fields[6] == "Sí" or fields[6] == "Si" or fields[6] == "sí" or fields[6] == "si":
                    data_dict["info_clinica"] = True
                elif fields[6] == "No" or fields[6] == "no":
                    data_dict["info_clinica"] = False
                else:
                    data_dict["info_clinica"] = None

                data_dict["observaciones"] = fields[7]
                try:
                    form = PatientForm(data_dict)
                    if form.is_valid():
                        form.save()
                        aux += 1
                    else:
                        messages.error(request, 'El archivo cargado presenta errores.')
                except Exception as e:
                    messages.error(request, 'El archivo cargado presenta errores.')
                    pass

    except Exception as e:
        messages.error(request, "Error al cargar archivo. Consulte el administrador. "+ repr(e))

    if aux == len(lines):
        messages.error(request, 'El archivo fue cargador correctamente.')
    return HttpResponseRedirect(reverse("patient:patient_upload"))
