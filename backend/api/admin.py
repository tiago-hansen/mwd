from django.contrib import admin

from .models import (
    Student, 
    UndergraduateProgram, 
    Course, 
    Enrollment,
)

admin.site.register(Student)
admin.site.register(UndergraduateProgram)
admin.site.register(Course)
admin.site.register(Enrollment)
