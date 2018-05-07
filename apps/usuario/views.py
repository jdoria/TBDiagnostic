from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from apps.usuario.forms import RegistroForm
from django.shortcuts import render
from django.contrib import messages
import json

# Create your views here.


# class RegistroUsuario(CreateView):
#     model = User
#     template_name = "usuario/registrar.html"
#     form_class = RegistroForm
#     success_url = reverse_lazy('login')

#User register view
def RegistroUsuario(request):
	if request.method == 'POST':
		username = request.POST['username']
		email = request.POST['email']
		password1 = request.POST['password1']
		password2 = request.POST['password2']
		try:
			user = User.objects.get(username=username)
			messages.error(request,'El usuario ya existe')
			print("EXISTE")
		except User.DoesNotExist:
			user = User.objects.create_user(username, email, password1)
			user.save()
			return redirect('login')
		

	return render(request, 'usuario/registrar.html')

