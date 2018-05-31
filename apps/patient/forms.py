from django import forms

from apps.patient.models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient

        opciones = (
            (None, 'No hay información'),
            (True, 'Sí'),
            (False, 'No'),
        )

        opciones_sexo = (
            (None, 'No hay información'),
            (True, 'Masculino'),
            (False, 'Femenino'),
        )

        opciones2 = (
            (True, 'Sí'),
            (False, 'No'),
        )

        fields = [
            'codigo',
            'edad',
            'sexo',
            'vih',
            'diabetes',
            'hab_calle',
            'info_clinica',
            'observaciones',
            'validacion',
        ]

        labels = {
            'codigo': 'Código',
            'edad': 'Edad',
            'sexo': 'Sexo',
            'vih': '¿Tiene VIH/AIDS?',
            'diabetes': '¿Tiene diabetes?',
            'hab_calle': '¿Es habitante de calle?',
            'info_clinica': 'Información Clínica',
            'observaciones': 'Observaciones',
            'validacion': 'Validación',
        }
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'sexo': forms.Select(choices=opciones_sexo),
            'vih': forms.Select(choices=opciones),
            'diabetes': forms.Select(choices=opciones),
            'hab_calle': forms.Select(choices=opciones),
            'info_clinica': forms.Select(choices=opciones),
            'observaciones': forms.TextInput(attrs={'class': 'form-control'}),
            'validacion': forms.Select(choices=opciones2),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']
        if Patient.objects.filter(codigo=codigo).exists():
            raise ValidationError("El código ya existe")
        return codigo
