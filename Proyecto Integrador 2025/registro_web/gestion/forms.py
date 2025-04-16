from django import forms
from .models import Docente, Estudiante

class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = '__all__'

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = '__all__'
