from django import forms


class LoginPoliciaForm(forms.Form):
    rut = forms.CharField(label="RUT", max_length=10)
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput
    )