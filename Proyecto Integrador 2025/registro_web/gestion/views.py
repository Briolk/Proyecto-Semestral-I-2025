


from django.shortcuts import render, redirect
from .forms import DocenteForm, EstudianteForm
from .models import Docente
from .models import Estudiante

def registrar_docente(request):
    if request.method == 'POST':
        form = DocenteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registro_docente')
    else:
        form = DocenteForm()

    docentes = Docente.objects.all()  # Obtén todos los docentes
    return render(request, 'registro_docente.html', {'form': form, 'docentes': docentes})

def registrar_estudiante(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registro_estudiante')
    else:
        form = EstudianteForm()
    
    estudiantes = Estudiante.objects.all()
    return render(request, 'registro_estudiante.html', {'form': form, 'estudiantes': estudiantes})

