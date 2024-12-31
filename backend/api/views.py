from django.shortcuts import render
from rest_framework import viewsets

from .serializers import (
    StudentSerializer,
    UndergraduateProgramSerializer,
    CourseSerializer,
    EnrollmentSerializer,
)

from .models import (
    Student,
    UndergraduateProgram,
    Course,
    Enrollment,
)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class UndergraduateProgramViewSet(viewsets.ModelViewSet):
    queryset = UndergraduateProgram.objects.all()
    serializer_class = UndergraduateProgramSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
