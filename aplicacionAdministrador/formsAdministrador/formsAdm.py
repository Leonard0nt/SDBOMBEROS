from django import forms
from aplicacionAdministrador.models import voluntarios, cuarteles, unidades # Asegúrate de importar tu modelo Voluntario y cualquier otro modelo necesario
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.shortcuts import redirect


def validar_rut(rut):
        rut = rut.replace(".", "").replace("-", "")
        if not rut[:-1].isdigit():
            return False
    
        rut, dv = rut[:-1], rut[-1]
        suma = 0
        mul = 2
    
        for d in reversed(rut):
            suma += int(d) * mul
            mul = (mul + 1) if mul < 7 else 2
    
        resultado = str((11 - (suma % 11)) % 11)
        return resultado == dv.upper() or (resultado == "K" and dv.upper() == "0")

class VoluntarioForm(forms.ModelForm):
    class Meta:
        model = voluntarios
        fields = ['rut','password','nombres','apellidos','cargo','telefono','compania','numero_registro','direccion']  # Utiliza '__all__' para incluir todos los campos del modelo en el formulario
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 2}),
        }
    # Puedes personalizar el formulario si es necesario
    # Por ejemplo, puedes agregar validaciones adicionales, widgets, etc.
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['rut']  # Establece el username como el rut

         # Establece la contraseña utilizando set_password
        password = self.cleaned_data.get('password')
        user.set_password(password)

        if commit:
            user.save()
        return user

    # Agrega una validación personalizada para el campo 'rut'
    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        rut_sin_puntos = rut.replace(".", "")
        if not validar_rut(rut_sin_puntos):
            raise forms.ValidationError('Rut inválido')
        return rut_sin_puntos



class UnidadForm(forms.ModelForm):
    class Meta:
        model = unidades
        fields = ['nomenclatura','patente','especialidad','cuartel_actual_uni','comentario']  # Utiliza '__all__' para incluir todos los campos del modelo en el formulario
        cuartel_actual_uni = forms.ModelChoiceField(queryset=cuarteles.objects.all(), required=True)
    # Agrega un widget para el campo 'comentario' para que sea un textarea
        widgets = {
            'comentario': forms.Textarea(attrs={'rows': 2}),
        }



