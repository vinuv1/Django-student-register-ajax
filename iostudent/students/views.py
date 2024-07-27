from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .forms import StudentForm
from .models import Student
import csv
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def student_registration(request):
    form = StudentForm()
    return render(request, 'register.html', {'form': form})

def ajax_register(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False})

def export_students_csv(request):
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(['First Name', 'Last Name', 'Email', 'Date of Birth', 'USN', 'Course'])

    students = Student.objects.all().values_list('first_name', 'last_name', 'email', 'date_of_birth', 'usn', 'course')
    for student in students:
        writer.writerow(student)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'
    return response

def export_students_pdf(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "Student List")
    p.setFont("Helvetica", 12)
    p.drawString(100, 735, "==================")

    p.setFont("Helvetica-Bold", 10)
    headers = ["First Name", "Last Name", "Email", "Date of Birth", "USN", "Course"]
    y = 710
    x_offsets = [50, 110, 200, 340, 450, 550]

    for index, header in enumerate(headers):
        p.drawString(x_offsets[index], y, header)

    p.setFont("Helvetica", 10)
    y = 690
    students = Student.objects.all()
    for student in students:
        p.drawString(x_offsets[0], y, student.first_name)
        p.drawString(x_offsets[1], y, student.last_name)
        p.drawString(x_offsets[2], y, student.email)
        p.drawString(x_offsets[3], y, str(student.date_of_birth))
        p.drawString(x_offsets[4], y, student.usn)
        p.drawString(x_offsets[5], y, student.course)
        y -= 15
        if y < 50:
            p.showPage()
            p.setFont("Helvetica", 10)
            y = 750
            for index, header in enumerate(headers):
                p.drawString(x_offsets[index], y, header)
            y -= 15

    p.showPage()
    p.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="students.pdf"'
    return response
