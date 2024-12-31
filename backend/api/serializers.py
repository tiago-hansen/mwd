from rest_framework import serializers
from .models import (
    Student, 
    UndergraduateProgram, 
    Course, 
    Enrollment,
)

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class UndergraduateProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = UndergraduateProgram
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'