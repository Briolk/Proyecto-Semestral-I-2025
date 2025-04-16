from django.urls import path
from . import views

urlpatterns = [
    path('docente/', views.registrar_docente, name='registro_docente'),
    path('estudiante/', views.registrar_estudiante, name='registro_estudiante'),
]
