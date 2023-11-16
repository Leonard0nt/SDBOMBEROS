from django.contrib import admin as admin
from aplicacionAdministrador.models import *


# Register your models here.

class excludeElementVoluntarios(admin.ModelAdmin):
    exclude = ('estado','unidad_asignada','cuartel_actual')

class excludeElementUnidades(admin.ModelAdmin):
    exclude = ('estado_unidad','comentario','cuartel_actual')

class excludeElementAdm(admin.ModelAdmin):
    exlude = ('cuartel_seleccionado',)    


admin.site.register(voluntarios, excludeElementVoluntarios)
admin.site.register(cuarteles)
admin.site.register(unidades, excludeElementUnidades)


