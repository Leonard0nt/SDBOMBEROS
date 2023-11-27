from django.shortcuts import render,redirect, get_object_or_404
from aplicacionAdministrador.models import *
from .formsAdministrador.formsAdm import VoluntarioForm, UnidadForm, EmergenciaForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from aplicacionVoluntarios import views as viewsVoluntario
from django.http import HttpResponse
from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView

from django.template.loader import render_to_string
from django.template.loader import get_template

from weasyprint import HTML


# Create your views here.


@login_required
def homeAdm(request):
    VoluntarioBuscado = request.user
    cuartelesBuscado= cuarteles.objects.all()
    img = "../static/Bomberos.png"
    for cuartel in cuartelesBuscado:
       cuartel.voluntarios_in = voluntarios.objects.filter(cuartel_actual_vol = cuartel.idCuartel, estado = True ).count()
       cuartel.unidades_in = unidades.objects.filter(cuartel_actual_uni = cuartel.idCuartel, estado_unidad = True).count()
       cuartel.conductores_in = voluntarios.objects.filter(cuartel_actual_vol = cuartel.idCuartel, estado = True ,conductor = True).count()

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
    else:
        form = VoluntarioForm()
    
    return render(request, '../templates/templatesAdministrador/agregarVoluntario.html',{'form':form})


def login(request):
    return render(request, '../templates/iniciarSesion.html', {'form': LoginView.form_class()})

class CustomLoginView(LoginView):
    template_name = '../templates/iniciarSesion.html'  # Ajusta según tu estructura de carpetas
    success_url = reverse_lazy('/')  # Ajusta según tu URL de redirección exitosa

    def get_success_url(self):
        # Verifica si el usuario es administrador y redirige en consecuencia
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return '/administrador/'  # Ajusta según tu URL de administrador
            else:
                return '/voluntario/'  # Ajusta según tu URL de voluntario
        return '/'

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if not any(message.tags == messages.ERROR for message in messages.get_messages(self.request)):
            messages.error(self.request, 'Credenciales incorrectas. Por favor, inténtalo de nuevo.')  # Mensaje de error
        return response
    


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

def admEmergencias(request):
    voluntariosEmer = voluntarios.objects.all()
    unidadesEmer = unidades.objects.all()
    emergenciasEmer = emergencias.objects.filter(EmergenciaActiva = True)

    data = {
        'voluntarios': voluntariosEmer,
        'unidades': unidadesEmer,
        'emergencias' : emergenciasEmer,
    }
    return render(request, '../templates/templatesAdministrador/emergencias.html',data)

def admOrganizarEmergencias(request,id_emergencia):
    emergenciaEmer = id_emergencia
    voluntariosEmer = voluntarios.objects.filter(estado = True)
    cuartelesEmer = cuarteles.objects.all()

    for cuartel in cuartelesEmer:
       cuartel.voluntarios_in = voluntarios.objects.filter(cuartel_actual_vol = cuartel.idCuartel, estado = True ).count()
       cuartel.unidades_in = unidades.objects.filter(cuartel_actual_uni = cuartel.idCuartel, estado_unidad = True).count()
       cuartel.conductores_in = voluntarios.objects.filter(cuartel_actual_vol = cuartel.idCuartel, estado = True ,conductor = True).count()
    
    unidadesEmer = unidades.objects.filter(estado_unidad = True)

    data = {
        'voluntarios': voluntariosEmer,
        'cuarteles': cuartelesEmer,
        'unidades': unidadesEmer,
        'emergencia': emergenciaEmer
    }
    return render(request, '../templates/templatesAdministrador/organizarEmergencia.html',data)

def admEmergenciaDatos(request):
    if request.method == 'POST':
        form = EmergenciaForm(request.POST)
        if form.is_valid():
            emergencia = form.save()
            # Redirigir a emergenciasDetalle con el ID de la nueva emergencia
            return redirect('organizarEmergencia' ,id_emergencia=emergencia.id_emergencia)
            
    else:
        form = EmergenciaForm()
        
        
        
    voluntariosEmer = voluntarios.objects.filter(estado = True)
    cuartelesEmer = cuarteles.objects.all()
    for cuartel in cuartelesEmer:
       cuartel.voluntarios_in = voluntarios.objects.filter(cuartel_actual_vol = cuartel.idCuartel, estado = True ).count()
       cuartel.unidades_in = unidades.objects.filter(cuartel_actual_uni = cuartel.idCuartel, estado_unidad = True).count()
       cuartel.conductores_in = voluntarios.objects.filter(cuartel_actual_vol = cuartel.idCuartel, estado = True ,conductor = True).count()
    
    unidadesEmer = unidades.objects.filter(estado_unidad = True)

    data = {
        'voluntarios': voluntariosEmer,
        'cuarteles': cuartelesEmer,
        'unidades': unidadesEmer,
    }
    


    return render(request, '../templates/templatesAdministrador/emergenciaDatos.html', {'form': form, **data})


def emergenciasDetalle(request,id_emergencia):
    emergencia = emergencias.objects.get(id_emergencia = id_emergencia)
    unidadesEmer = unidades.objects.filter(emergencia_atendida = id_emergencia)
    
    unidadesID = []
    for unidad in unidadesEmer:
        unidadesID.append(unidad.nomenclatura)

    voluntariosEmer = voluntarios.objects.filter(unidad_asignada__in=unidadesID)


    data = {
        'voluntarios': voluntariosEmer,
        'unidades': unidadesEmer,
        'emergencia' : emergencia,
    }
    return render(request, '../templates/templatesAdministrador/emergenciasDetalles.html',data)

def emergenciasCompletar(request,id_emergencia):
    emergencia = emergencias.objects.get(id_emergencia = id_emergencia)
    unidadesEmer = unidades.objects.filter(emergencia_atendida = id_emergencia)
    
    unidadesID = []
    for unidad in unidadesEmer:
        unidadesID.append(unidad.nomenclatura)

    voluntariosEmer = voluntarios.objects.filter(unidad_asignada__in = unidadesID)

    for voluntario in voluntariosEmer:
        voluntario.unidad_asignada = ''
        voluntario.estado = True
        voluntario.save()

    emergencia.EmergenciaActiva = False
    emergencia.save()

    for unidad in unidadesEmer:
        unidad.estado_unidad = True
        unidad.estado_unidad = True
        unidad.emergencia_atendida = 0
        unidad.save()

    return redirect(admEmergencias)


def asignarAUnidades(request, nomenclatura, id_emergencia):
    unidad = unidades.objects.get(nomenclatura=nomenclatura)
    unidad.estado_unidad = False 
    unidad.emergencia_atendida = id_emergencia
    unidad.save()

    if request.method == 'POST':
        ruts_seleccionados = request.POST.getlist('SelectVoluntarios')
        for rut in ruts_seleccionados:
            voluntario = voluntarios.objects.get(rut=rut)
            voluntario.unidad_asignada = nomenclatura
            voluntario.estado = False
            voluntario.save()
    
    return redirect(admOrganizarEmergencias, id_emergencia=id_emergencia)

def despachar(request,id_emergencia):
    emergencia = emergencias.objects.get(id_emergencia=id_emergencia)
    unidadesEmer = unidades.objects.filter(emergencia_atendida = id_emergencia)
    unidadesID = []
    for unidad in unidadesEmer:
        unidadesID.append(unidad.nomenclatura)

    voluntariosEmer = voluntarios.objects.filter(unidad_asignada__in=unidadesID).count()

    emergencia.unidades_in_emer = unidades.objects.filter(emergencia_atendida = id_emergencia).count()
    emergencia.voluntarios_in_emer = voluntariosEmer
    emergencia.save()

    return redirect(admEmergencias)


def generate_pdf(request):
    emergenciaEmer = emergencias.objects.all()

    logo_path = "../static/Bomberos.png"
    
    # Obtén los datos que quieres mostrar en el PDF
    data = {
        'emergencias' : emergenciaEmer,
        'logo_path' : logo_path,
        # Agrega más datos según sea necesario
    }

    # Renderiza la plantilla a HTML
    template = get_template('../templates/templatesAdministrador/generarPdf.html')
    html = template.render(data)

    # Crea un objeto HTML de WeasyPrint
    response = HttpResponse(content_type='application/pdf')
    HTML(string=html).write_pdf(response)

    return response


        
    
