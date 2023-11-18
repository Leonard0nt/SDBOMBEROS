from django.shortcuts import render,redirect, get_object_or_404
from aplicacionAdministrador.models import *
from .formsAdministrador.formsAdm import VoluntarioForm, UnidadForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from aplicacionVoluntarios import views as viewsVoluntario
from django.http import JsonResponse
from django import forms
from django.contrib.auth.hashers import make_password
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
def administracionVoluntarios(request):
    adm = request.user
    voluntarios_list = voluntarios.objects.filter(is_staff=False)
    
    contexto = {
        'adm': adm,
        'voluntarios_list': voluntarios_list,
        }
    return render(request, "../templates/templatesAdministrador/administracionVoluntarios.html", contexto)

@login_required
def homeAdmCuartelUnidades(request,idCuartel):
    idCuartell = idCuartel
    img = "../static/Bomberos.png"
    adm = request.user
    unidadesCuartel = unidades.objects.filter(cuartel_actual_uni = idCuartell,estado_unidad = True)
    cuartelActual = cuarteles.objects.get(idCuartel=idCuartell)
    
    contexto = {
        'voluntario': adm,
        'unidadesCuartel': unidadesCuartel,
        'cuartel': cuartelActual,
        'img' : img,
        }
    return render(request, "../templates/templatesAdministrador/cuartelUnidades.html", contexto)

@login_required
def administracionUnidades(request):
    cuartelesUni = cuarteles.objects.all()
    img = "../static/Bomberos.png"
    adm = request.user
    unidadesAdm = unidades.objects.all()
    
    contexto = {
        'cuarteles': cuartelesUni,
        'voluntario': adm,
        'unidadesAdm': unidadesAdm,
        'img' : img,
        }
    return render(request, "../templates/templatesAdministrador/administracionUnidades.html", contexto)

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


def editar_voluntarioADM(request, rut):
    voluntario = get_object_or_404(voluntarios, rut=rut)
    
    if request.method == 'POST':
        voluntario.nombres = request.POST.get('nombres')
        voluntario.apellidos = request.POST.get('apellidos')
        voluntario.cargo = request.POST.get('cargo')
        voluntario.telefono = request.POST.get('telefono')
        voluntario.compania = request.POST.get('compania')
        voluntario.direccion = request.POST.get('direccion')
        conductor_value = request.POST.get('conductor')

        conductor_value = request.POST.get('conductor', False)
        voluntario.conductor = True if conductor_value else False


        voluntario.save()  # Guarda el cambio en la base de datos

        return redirect(administracionVoluntarios)



def eliminar_voluntario(request, rut):
    voluntario = get_object_or_404(voluntarios, rut=rut)
    
    voluntario.delete()

    return redirect(administracionVoluntarios)


def cambiar_password_vol(request,rut):
    voluntario = get_object_or_404(voluntarios, rut=rut)

    if request.method == 'POST':
        voluntario.set_password(request.POST.get('nueva_contrasena'))
        voluntario.save()
    
    return redirect(administracionVoluntarios)

def editar_unidadADM(request, nomenclatura):
    unidad = get_object_or_404(unidades, nomenclatura=nomenclatura)

    if request.method == 'POST':
        unidad.especialidad = request.POST.get('especialidad')
        cuartelid = request.POST.get('cuartel_actual_uni')
        cuartel = cuarteles.objects.get(idCuartel = cuartelid)
        unidad.cuartel_actual_uni = cuartel
        unidad.comentario= request.POST.get('comentario')


        estado_value = request.POST.get('disponibilidad', False)
        unidad.estado_unidad = True if estado_value else False


        unidad.save()  # Guarda el cambio en la base de datos

        return redirect(administracionUnidades)

def eliminar_unidadADM(request,nomenclatura):
    unidad = get_object_or_404(unidades, nomenclatura=nomenclatura)

    unidad.delete()

    return redirect(administracionUnidades)