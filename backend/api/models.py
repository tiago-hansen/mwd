from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    registration = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class UndergraduateProgram(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.code


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    undergraduate_program = models.ForeignKey(UndergraduateProgram, on_delete=models.CASCADE)
    SEMESTER_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    ]
    semester = models.IntegerField(choices=SEMESTER_CHOICES)

    def __str__(self):
        return self.code


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.registration} - {self.course.code} - {self.grade}'
