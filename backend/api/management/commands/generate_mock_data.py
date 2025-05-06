import random

from django.core.management.base import BaseCommand
from faker import Faker
import numpy as np

from api.models import (
    Student, 
    UndergraduateProgram, 
    Course, 
    Enrollment,
)

fake = Faker()

class Command(BaseCommand):
    help = 'Generate mock data for the database'

    def handle(self, *args, **kwargs):
        '''
        Generate mock data for all models
        '''
        self.generate_students()
        self.generate_undergraduate_programs()
        self.generate_courses()
        self.generate_enrollments()

    def generate_students(self):
        '''
        Generate 30 students with random data
        '''
        for _ in range(30):
            student = Student.objects.create(
                name=fake.name(),
                email=fake.email(),
                registration=fake.unique.random_number(digits=8),
            )
            self.stdout.write(self.style.SUCCESS(f'Created student {student.name}'))

    def generate_undergraduate_programs(self):
        '''
        Generate 7 predefined undergraduate programs
        '''
        UNDERGRAD_PROGRAMS = {
            'ECA': 'Engenharia de Controle e Automação',
            'EPS': 'Engenharia de Produção',
            'EMC': 'Engenharia Mecânica',
            'EMT': 'Engenharia de Materiais',
            'EEL': 'Engenharia Elétrica',
            'ELT': 'Engenharia Eletrônica',
            'EQA': 'Engenharia Química',
        }
        for code, name in UNDERGRAD_PROGRAMS.items():
            program = UndergraduateProgram.objects.create(
                name=name,
                code=code,
            )
            self.stdout.write(self.style.SUCCESS(f'Created undergraduate program {program.code}'))
    
    def generate_courses(self):
        '''
        Generate 70 courses with random data
        '''
        for _ in range(70):
            course = Course.objects.create(
                name=fake.word(),
                code=fake.unique.random_number(digits=5),
                undergraduate_program=UndergraduateProgram.objects.order_by('?').first(),
                semester=random.randint(1, 10),
            )
            self.stdout.write(self.style.SUCCESS(f'Created course {course.code}'))
    
    def generate_enrollments(self):
        '''
        Generate 700 enrollments with random data
        '''
        for _ in range(700):
            student = Student.objects.order_by('?').first()
            course = Course.objects.order_by('?').first()
            grade = round(np.random.normal(6, 1.5), 2) # Normal distribution with mean 6 and std 1.5
            date = fake.date_time_this_year()
            Enrollment.objects.create(
                student=student,
                course=course,
                grade=grade if grade <= 10 else 10, # Limit grade to 10
                date=date
            )
            self.stdout.write(self.style.SUCCESS(f'Created enrollment for {student.name} in {course.code}'))