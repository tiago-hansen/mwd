from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Avg


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

    # Override the list method to filter courses by program
    def list(self, request):
        params = request.query_params
        program_code = params.get('program_code')

        if program_code:
            queryset = self.queryset.filter(undergraduate_program__code=program_code)
            if not queryset.exists():
                return Response({"message": "No courses found for this program."}, status=404)
        else:
            queryset = self.queryset.all()

        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    # Create custom endpoint to calculate average grade for a course
    @action(detail=False, methods=['get'])
    def average_grade(self, request):
        params = request.query_params
        course_code = params.get('course_code')
        enrollments = self.queryset.all()

        if course_code:
            enrollments = self.queryset.filter(course__code=course_code)

        if not enrollments.exists():
            return Response({"message": "No enrollments found."}, status=404)

        average_grade = enrollments.aggregate(average_grade=Avg('grade'))['average_grade']

        return Response({"average_grade": average_grade})
