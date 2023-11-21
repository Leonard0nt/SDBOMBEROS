import base64
from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from aplicacionAdministrador.models import *
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from aplicacionVoluntarios.formsVoluntario.formsVol import VoluntarioEditForm
from aplicacionVoluntarios.formsVoluntario.formsVolPass import ContrasenaEditForm



# Create your views here.
img = "../static/Bomberos.png" 

@login_required    
def homeVoluntarios(request):
    cuartelesBuscado= cuarteles.objects.all()
    VoluntarioBuscado = request.user
    contexto = {'img': img,'voluntario':VoluntarioBuscado,'cuarteles': cuartelesBuscado,}
    return render(request,  "../templates/templatesVoluntario/indexVoluntario.html",contexto)

def obtener_opciones_cuartel(request):
    cuarteles = cuarteles.objects.all()  # Obtengo todos los cuarteles en una variable
    data = [{'id': cuartel.idCuartel, 'nombre': cuartel.nombre_cuartel} for cuartel in cuarteles] #Extraigo el id y el nombre de cada cuartel 
    return JsonResponse(data, safe=False)


def actualizar_estado_voluntario(request):
    #cambio de estado
    if request.method == 'POST':
        nvoestado = request.POST.get('options-outlined')  # obtengo el valor del boton clickeado

        voluntario = request.user

        if nvoestado == 'disp':
            voluntario.estado = True  # Si el boton devuelve que se marco disp se activa la disponibilidad
        else:
            voluntario.estado = False  # caso contrario por defecto se desactiva la disponibilidad

        voluntario.save()  # Guarda el cambio en la base de datos

        return redirect(homeVoluntarios)
    
def actualizar_cuartel_voluntario(request):
    #cambio de cuartel
    if request.method == 'POST':
        nvoCuartel = request.POST.get('cuartelActual') # Obtengo el id del nuevo cuartel extraido del boton clickeado 
        cuartelNvo = cuarteles.objects.get(idCuartel = nvoCuartel) # busco y asigno el nuevo cuartel a una variable
        voluntario = request.user # busco el voluntario actual usando la app

        voluntario.cuartel_actual_vol = cuartelNvo # cambio la fk del cuartel por la extraida anteriormente

        voluntario.save() # guardo los cambios

        return redirect(homeVoluntarios)
    
def actualizar_disp_cuart(request): # funcion que realiza el cambio de disponibilidad y cuartel a la vez
    actualizar_estado_voluntario(request)
    actualizar_cuartel_voluntario(request)

    return redirect(homeVoluntarios)


    
def verCuartelActual(request,idCuartel):
    idCuartell = idCuartel
    VoluntarioBuscado = request.user
    cuartelesBuscado= cuarteles.objects.get(idCuartel=idCuartell)
    cuartelesBuscado.voluntarios_in = voluntarios.objects.filter(cuartel_actual_vol = idCuartell, estado = True ).count()
    cuartelesBuscado.unidades_in = unidades.objects.filter(cuartel_actual_uni = idCuartell, estado_unidad = True ).count()
    contexto = {
        'voluntario': VoluntarioBuscado,
        'cuartel': cuartelesBuscado,
        'img' : img,
        }
    return render(request, "../templates/templatesVoluntario/cuartelActualInfo.html", contexto)


def edit_voluntario(request, rut):
    voluntario = get_object_or_404(voluntarios, rut=rut)
    
    if request.method == 'POST':
        form = VoluntarioEditForm(request.POST, instance=voluntario)
        if form.is_valid():
            form.save()
            return redirect(reverse('voluntario'))
    else:
        form = VoluntarioEditForm(instance=voluntario)

    return render(request, '../templates/templatesVoluntario/configPerfil.html', {'form': form, 'voluntario': voluntario})


def edit_contrasena(request, rut):
    voluntario = get_object_or_404(voluntarios, rut=rut)
    
    if request.method == 'POST':
        form = ContrasenaEditForm(request.POST, instance=voluntario)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
    else:
        form = ContrasenaEditForm(instance=voluntario)

    return render(request, '../templates/templatesVoluntario/cambiarContra.html', {'form': form, 'voluntario': voluntario})