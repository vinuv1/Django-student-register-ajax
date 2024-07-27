from django.db import models

class Student(models.Model):
    COURSE_CHOICES = [
        ('PY', 'Python'),
        ('MA', 'Mathematics'),
        ('JV', 'Java'),
        ('RB', 'Ruby'),
        ('BT', 'Biotechnology'),
        ('MBA', 'MBA'),
        # Add more courses as needed
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    usn = models.CharField(max_length=20, unique=True)
    course = models.CharField(max_length=10, choices=COURSE_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
