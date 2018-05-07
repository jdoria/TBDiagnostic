from import_export import resources, fields
from import_export.widgets import IntegerWidget, Widget
from apps.patient.models import Patient


class MyBoolWidget(Widget):
    TRUE_VALUES = ["1", "True", "Sí", 1]
    FALSE_VALUE = ["0", "False", "No"]

    def render(self, value, obj=None):
        if value is None:
            return "No hay información"
        return self.TRUE_VALUES[2] if value else self.FALSE_VALUE[2]

    def clean(self, value, row=None, *args, **kwargs):
        if value is None:
            return None
        return True if value in self.TRUE_VALUES else False


class SexoWidget(Widget):
    TRUE_VALUES = ["1", "True", "Masculino", 1]
    FALSE_VALUE = ["0", "False", "Femenino"]

    def render(self, value, obj=None):
        if value is None:
            return "No hay información"
        return self.TRUE_VALUES[2] if value else self.FALSE_VALUE[2]

    def clean(self, value, row=None, *args, **kwargs):
        if value is None:
            return None
        return True if value in self.TRUE_VALUES else False


class PatientResource(resources.ModelResource):
    codigo = fields.Field(column_name='Código', attribute='codigo')
    sexo = fields.Field(column_name='Sexo', attribute='sexo', widget=SexoWidget())
    edad = fields.Field(column_name='Edad', attribute='edad', widget=IntegerWidget())
    vih = fields.Field(column_name='¿Tiene VIH/AIDS?', attribute='vih', widget=MyBoolWidget())
    diabetes = fields.Field(column_name='¿Tiene diabetes?', attribute='diabetes', widget=MyBoolWidget())
    hab_calle = fields.Field(column_name='¿Es habitante de calle?', attribute='hab_calle', widget=MyBoolWidget())
    info_clinica = fields.Field(column_name='Información Clínica', attribute='info_clinica', widget=MyBoolWidget())
    observaciones = fields.Field(column_name='Observaciones', attribute='observaciones')
    fecha_creacion = fields.Field(column_name='Fecha de creación', attribute='fecha_creacion')

    class Meta:
        model = Patient
        fields = (
            'codigo',
            'edad',
            'sexo',
            'vih',
            'diabetes',
            'hab_calle',
            'info_clinica',
            'observaciones',
            'fecha_creacion',
        )
        export_order = fields
