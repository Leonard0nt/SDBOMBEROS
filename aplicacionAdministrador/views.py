from django.shortcuts import render,redirect, get_object_or_404
from aplicacionAdministrador.models import *
from .formsAdministrador.formsAdm import VoluntarioForm, UnidadForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from aplicacionVoluntarios import views as viewsVoluntario
from django.http import JsonResponse
from django.contrib.auth.views import LoginView
# Create your views here.

@login_required
def homeAdm(request):
    VoluntarioBuscado = request.user
    cuartelesBuscado= cuarteles.objects.all()
    img = "../static/Bomberos.png"
    for cuartel in cuartelesBuscado:
       cuartel.voluntarios_in = voluntarios.objects.filter(cuartel_actual_vol = cuartel.idCuartel, estado = True ).count()
       cuartel.unidades_in = unidades.objects.filter(cuartel_actual_uni = cuartel.idCuartel, estado_unidad = True).count()

    contexto = {
    'voluntario': VoluntarioBuscado,
    'cuarteles': cuartelesBuscado,
    'img': img,
    }
    return render(request, "../templates/templatesAdministrador/indexAdm.html", contexto)

@login_required
def homeAdmCuartel(request,idCuartel):
    idCuartell = idCuartel
    VoluntarioBuscado = request.user
    cuartelesBuscado= cuarteles.objects.get(idCuartel=idCuartell)
    cuartelesBuscado.voluntarios_in = voluntarios.objects.filter(cuartel_actual_vol = idCuartell, estado = True ).count()
    cuartelesBuscado.unidades_in = unidades.objects.filter(cuartel_actual_uni = idCuartell, estado_unidad = True ).count()
    contexto = {
        'voluntario': VoluntarioBuscado,
        'cuartel': cuartelesBuscado,
        }
    return render(request, "../templates/templatesAdministrador/indexAdmCuartel.html", contexto)

@login_required
def homeAdmCuartelVoluntarios(request,idCuartel):
    idCuartell = idCuartel
    adm = request.user
    voluntariosCuartel = voluntarios.objects.filter(cuartel_actual_vol = idCuartell, estado = True)
    cuartelActual = cuarteles.objects.get(idCuartel=idCuartell)
    
    contexto = {
        'voluntario': adm,
        'voluntariosCuartel': voluntariosCuartel,
        'cuartel': cuartelActual,
        }
    return render(request, "../templates/templatesAdministrador/cuartelVoluntarios.html", contexto)

@login_required
def homeAdmCuartelUnidades(request,idCuartel):
    idCuartell = idCuartel
    img = "../static/Bomberos.png"
    adm = request.user
    unidadesCuartel = unidades.objects.filter(cuartel_actual_uni = idCuartell)
    cuartelActual = cuarteles.objects.get(idCuartel=idCuartell)
    
    contexto = {
        'voluntario': adm,
        'unidadesCuartel': unidadesCuartel,
        'cuartel': cuartelActual,
        'img' : img,
        }
    return render(request, "../templates/templatesAdministrador/cuartelUnidades.html", contexto)

@login_required
def agregarVoluntario(request):
    form = VoluntarioForm()
    if request.method == 'POST':
        form = VoluntarioForm(request.POST)
        if form.is_valid():
            form.save()
        return homeAdm(request)
    data = {'form':form}
    return render(request, '../templates/templatesAdministrador/agregarVoluntario.html',data)


def login(request):
    return render(request, '../templates/iniciarSesion.html', {'form': LoginView.form_class()})

class CustomLoginView(LoginView):
    template_name = '../templates/iniciarSesion.html'  # Ajusta según tu estructura de carpetas

    def get_success_url(self):
        # Verifica si el usuario es administrador y redirige en consecuencia
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return '/administrador/'  # Ajusta según tu URL de administrador
            else:
                return '/voluntario/'  # Ajusta según tu URL de voluntario
        return '/'


def agregarUnidad(request):
    if request.method == 'POST':
        form = UnidadForm(request.POST)
        if form.is_valid():
            form.save()
        return homeAdm(request)
    else:
        form = UnidadForm()

    return render(request, '../templates/templatesAdministrador/agregarUnidad.html', {'form': form})










