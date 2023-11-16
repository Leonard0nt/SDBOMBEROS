"""
URL configuration for sistema_disponibilidad_bomberos_parral project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from aplicacionVoluntarios import views as viewVoluntario
from aplicacionAdministrador import views as viewAdm
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('voluntario/', viewVoluntario.homeVoluntarios, name="voluntario"),
    path('administrador/', viewAdm.homeAdm),
    path('actualizar_estado_voluntario/', viewVoluntario.actualizar_estado_voluntario, name='actualizar_estado_voluntario'),
    path('actualizar_disp_cuart/', viewVoluntario.actualizar_disp_cuart, name='actualizar_disp_cuart'),
    path('administrarCuartel/<int:idCuartel>/', viewAdm.homeAdmCuartel, name='administrarCuartel'),
    path('cuartelVoluntarios/<int:idCuartel>/', viewAdm.homeAdmCuartelVoluntarios, name='cuartelVoluntarios'),
    path('cuartelUnidades/<int:idCuartel>/', viewAdm.homeAdmCuartelUnidades, name='cuartelUnidades'),
    path('agregarVoluntario/', viewAdm.agregarVoluntario, name='agregarVoluntario'),
    path('agregarUnidad/', viewAdm.agregarUnidad, name='agregarUnidad'),
    path('verInfoCuartelActual/<int:idCuartel>/',viewVoluntario.verCuartelActual, name='verInfoCuartelActual'),
    path('login/', viewAdm.CustomLoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(next_page='/login'), name='logout'),
    path('editar_voluntario/<str:rut>/', viewVoluntario.edit_voluntario, name='editar_voluntario'),
    path('', viewAdm.CustomLoginView.as_view(), name = 'login'),
]