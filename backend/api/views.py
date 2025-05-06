from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import (
    Avg,
    Count,
    Q,
)


from .serializers import (
    StudentSerializer,
    UndergraduateProgramSerializer,
    CourseSerializer,
    EnrollmentSerializer,
    AverageGradeSerializer,
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
        semester = params.get('semester')
        courses_queryset = self.queryset.all()

        if program_code:
            courses_queryset = courses_queryset.filter(
                undergraduate_program__code=program_code)

        if semester:
            try:
                semester = int(semester)
                courses_queryset = courses_queryset.filter(semester=semester)
            except ValueError:
                return Response({"message": "Invalid semester value."}, status=400)

        if not courses_queryset.exists():
            return Response({"message": "No courses found."}, status=404)

        serializer = CourseSerializer(courses_queryset, many=True)
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
            enrollments = enrollments.filter(course__code=course_code)

        if not enrollments.exists():
            return Response({"message": "No enrollments found."}, status=404)

        average_grade = enrollments.aggregate(
            average_grade=Avg('grade'))['average_grade']

        serializer = AverageGradeSerializer({"average_grade": average_grade})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_metrics_by_program(self, request):
        APPROVAL_GRADE = 5.75
        enrollments = self.queryset.all()
        if not enrollments.exists():
            return Response({"message": "No enrollments found."}, status=404)

        metrics = {}

        grouped_data = (
            enrollments.values('course__undergraduate_program__code',
                               'course__undergraduate_program__name')
            .annotate(
                average_grade=Avg('grade'),
                total_enrollments=Count('id'),
                failures=Count('id', filter=Q(grade__lt=APPROVAL_GRADE))
            )
            .order_by('course__undergraduate_program__code')
        )

        for data in grouped_data:
            program_code = data['course__undergraduate_program__code']
            program_name = data['course__undergraduate_program__name']
            failure_rate = (data['failures'] / data['total_enrollments']
                            ) if data['total_enrollments'] > 0 else 0
            if program_code not in metrics:
                metrics[program_code] = {
                    "program_name": program_name,
                    "average_grade": data['average_grade'],
                    "failure_rate": failure_rate
                }

        return Response(metrics)
