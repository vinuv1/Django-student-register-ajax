from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.student_registration, name='student_registration'),
    path('ajax_register/', views.ajax_register, name='ajax_register'),
    path('export/csv/', views.export_students_csv, name='export_students_csv'),
    path('export/pdf/', views.export_students_pdf, name='export_students_pdf'),
]
