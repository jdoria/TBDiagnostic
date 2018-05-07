from django.conf.urls import url
from apps.usuario.views import RegistroUsuario

app_name = 'usuario'

urlpatterns = [
	url(r'^registrar', RegistroUsuario, name = "registrar"),

]