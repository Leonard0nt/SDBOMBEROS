from django import forms
from aplicacionAdministrador.models import voluntarios
from django.contrib.auth.forms import UserChangeForm



class VoluntarioEditForm(forms.ModelForm):
    # Puedes agregar campos adicionales o personalizar según sea necesario
    class Meta:
        model = voluntarios
        fields = ['nombres', 'apellidos', 'telefono', 'compania', 'direccion', 'password']

    def save(self, commit=True):
        voluntario = super().save(commit=False)

        # Verificar si la contraseña ha cambiado antes de encriptarla
        if 'password' in self.changed_data:
            password = self.cleaned_data.get('password')
            voluntario.set_password(password)

        if commit:
            voluntario.save()

        return voluntario

    widgets = {
        'password': forms.PasswordInput(),
        'direccion': forms.Textarea(attrs={'rows':2,'class': 'form-control col-md-6'})
    }
           

