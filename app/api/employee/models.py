from django.db import models
from app.api.models import BaseModel
from ..authentication.helpers.user_helpers import create_username_slug
from ..authentication.models import User
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
# Create your models here.

"""
The Employee Database is a database that
comprises the details needed about an Employee
together with all its other related tables.
The database tables that are needed as of Aug 17, 2021
in order to make the employee database complete are:
    - Employer
    - Grade
    - Department
    - Employee
    - Full Time Emp
    - Part Time Emp
    - Seasonal Emp
    - Temporary Emp
    - Payroll
    - Receipt
    - Title
    - Courses

These tables interact with each other to create the 
employee database.
"""


class Employer(BaseModel):
    """
    This class(database table) is meant to define 
    the Employer who has employed the
    employees and holds a one to Many r/ship
    with his/her employees
    The fields pertaining to this class are:
        - business name(character field)
        - phone numbers(character field)
        - website link(url field)
        - address(character field)
        - contact person name(character field)
        - contact person phone number(character field)
        - contact person role/position(character field)
        - user representation(foreign key field)
        - location(character field)
        - industry(character field)
        - size(text field)
    """
    business_name = models.CharField(max_length=255, blank=True, null=True)
    phone_numbers = models.CharField(max_length=200, blank=True)
    website_link = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    contact_name = models.CharField(max_length=255, blank=True, null=True)
    contact_phone_number = models.CharField(max_length=255, blank=True, null=True)
    contact_role = models.CharField(max_length=255, blank=True, null=True)
    employer_details = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    industry = models.CharField(max_length=255, null=True, blank=True)
    size = models.TextField(blank=True, null=True)


class Grade(BaseModel):
    """
    This class(database table) has the pay grade of different employees
    and its relationship with both employees and department
    is one-to-many.
    The fields of this class are:
        - grade name(Character Field)  
        - grade basic(Character Field)
        - grade_da(Character Field)
        - grade_ta(Character Field)
        - grade bonus(Float Field)
        - grade pf(Character Field)
    """
    grade_name = models.CharField(max_length=255)
    grade_basic = models.CharField(max_length=255)
    grade_da = models.CharField(max_length=255)
    grade_ta = models.CharField(max_length=255)
    grade_bonus = models.FloatField()
    grade_pf = models.CharField(max_length=255)


class Department(BaseModel):
    """
    This class(database table) defines the 
    department that the employee belongs to.
    It holds a many to many relationship with
    the employee.
    The fields pertaining to this class are:
        - department name(character field)
        - pay_grade(foreignkey field)

    """
    department_name = models.CharField(max_length=255)
    pay_grade = models.ForeignKey(Grade, on_delete=models.CASCADE,
                                null=True, blank=True)


class Title(BaseModel):
    """
    This class(database table) defines the 
    job titles of the workers in the organization
    and can be added as many as one may want.
    The fields pertaining to this class are:
        - title name(text field) 
    """
    title_name = models.TextField()


class Course(BaseModel):
    """
    This class(database table) defines the
    courses that the employee has completed.
    And it is dynamic. 
    The fields pertaining to this class are
        - course name(text field)
        - course level(character field)
    """
    class LevelOptions(models.TextChoices):
        HIGH_SCHOOL = 'H', _('Form Four Certificate')
        DEGREE = 'DE', _('Degree')
        DIPLOMA = 'DI', _('Diploma')
        MASTERS = 'M', _('Masters')
        DOCTORATE = 'DO', _('PHD')
    course_name = models.TextField()
    course_level = models.CharField(max_length=10,
                                    choices=LevelOptions.choices,
                                    default=LevelOptions.DEGREE)

    class Meta:
        unique_together = ['course_name', 'course_level']


class Employee(BaseModel):
    """
    The employee class(database table) is meant to keep up to date
    records about the details of the employee.
    Details that shall be consistent throughout employees are:
        - first_name(character field)
        - last_name(character field)
        - other names(text field)
        - email(email field)
        - adress(character field)
        - phone numbers(character field )
        - emergency_contacts(array field)
        - date of birth(date field)
        - job title(character field)
        - manager's name(character field)
        - department(character field)
        - hiring date(date field)
        - current salary(float field)
        - starting salary(float field)
        - qualifications(array field)
        - period(character field)
        - per_period(float field)
        - rate per hour(integer field)
        - completed courses(text field)
        - recommendations(text field)
        - employee grade(character field)
        - status(character field choices)
        - reviews (to do)
        - recruitment (to do)
    """

    class StatusOptions(models.TextChoices):
        FULL_TIME = 'F', _('Full Time')
        PART_TIME = 'P', _('Part Time')
        CONTRACT = 'C', _('Contract')
        LAID_OFF = 'L', _('Laid Off')

    class PeriodOptions(models.TextChoices):
        DAILY = 'D', _('Daily')
        WEEKLY = 'W', _('Weekly')
        MONTHLY = 'M', _('Monthly')
        YEARLY = 'Y', _('Yearly')

    class GenderOptions(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')

    status = models.CharField(
        max_length=10,
        choices=StatusOptions.choices,
        default=StatusOptions.FULL_TIME,
        blank=False,
        null=False
    )

    gender = models.CharField(
        max_length=2,
        choices=GenderOptions.choices,
        default=GenderOptions.MALE,
        blank=False, unique=False
    )
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    other_names = models.TextField(blank=False)
    email = models.EmailField(blank=False)
    address = models.TextField(blank=False)
    phone_numbers = models.CharField(max_length=200, blank=True)
    emergency_numbers = models.CharField(max_length=200, blank=True)
    date_of_birth = models.DateField(blank=False)
    job_title = models.ForeignKey(Title, on_delete=models.CASCADE, null=True, blank=True)
    employer_name = models.ForeignKey(
        Employer, on_delete=models.CASCADE, blank=True, null=True)
    department = models.ManyToManyField(Department, blank=True)
    hiring_date = models.DateField()
    current_salary = models.FloatField()
    starting_salary = models.FloatField()
    qualifications = models.CharField(max_length=200, blank=True)
    completed_courses = models.ForeignKey(Course, on_delete=models.CASCADE,
                                        null=True, blank=True)
    rate_hour = models.FloatField(blank=True, null=True)
    period = models.CharField(max_length=10, choices=PeriodOptions.choices,
                            default=PeriodOptions.MONTHLY)
    per_period = models.FloatField(blank=True, null=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        """
        returns a string representation 
        of the model
        """
        return f"{self.first_name}-{self.last_name}-{self.other_names}"


class FullTimeEmployee(BaseModel):
    """
    This class(database table) defines the employees who 
    work past 30 hours in a week.
    The fields of this class are:
        - experience(text field)
        - projects completed (to do)
        - emp_id(foreignkey field)
    """
    experience = models.TextField()
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, null=True, blank=True)


class PartTimeEmployee(BaseModel):
    """
    This class(database table) defines the employees who 
    work less than 30 hours in a week 
        - period(character field)
        - period_number(integer field)
        - emp_id(foreign key field)
        - projects_completed (to do)
    """
    class PeriodOptions(models.TextChoices):
        DAY = 'D', _('Day(s)')
        WEEK = 'W', _('Week(s)')
        MONTH = 'M', _('Month(s)')
        YEAR = 'Y', _('Year(s)')

    period = models.CharField(max_length=10, choices=PeriodOptions.choices,
                              default=PeriodOptions.MONTH)
    period_number = models.IntegerField()
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, null=True, blank=True)


class TemporaryEmployee(BaseModel):
    """
    This class(database table) defines the employees who
    are onboarded into projects for specific tasks
    or entire projects. Tax is normally withheld from them
    The fields belonging to this class are:
        - project_name (to do)
        - period(character field)
        - period_number(integer field) 
        - emp_id(foreignkey field)
    """
    class PeriodOptions(models.TextChoices):
        DAY = 'D', _('Day(s)')
        WEEK = 'W', _('Week(s)')
        MONTH = 'M', _('Month(s)')
        YEAR = 'Y', _('Year(s)')

    period = models.CharField(max_length=10, choices=PeriodOptions.choices,
                              default=PeriodOptions.MONTH)
    period_number = models.IntegerField()
    project_name = models.TextField()
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, null=True, blank=True)


class SeasonalEmployee(BaseModel):
    """
    This class(database table) defines the employees who are onboarded
    during peak seasons like during holidays or harvest time
    The fields belonging to this class are:
        - season(character field)
        - project_name (text field)
        - period(character field)
        - period_number(integer field)
        - emp_id(foreign key field)
    """
    class PeriodOptions(models.TextChoices):
        DAY = 'D', _('Day(s)')
        WEEK = 'W', _('Week(s)')
        MONTH = 'M', _('Month(s)')
        YEAR = 'Y', _('Year(s)')

    period = models.CharField(max_length=10, choices=PeriodOptions.choices,
                              default=PeriodOptions.MONTH)
    period_number = models.IntegerField()
    season = models.TextField()
    project_name = models.TextField()
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, null=True, blank=True)
    season = models.TextField()


class Payroll(BaseModel):
    """
    This class(database table) defines the salary ranges 
    and details.
    The fields belonging to this class are:
        - emp_net_salary(float field) 
        - emp_gross_salary(float field)
        - reimbursment_date(date field)
        - transaction_id (to do )
        - emp_id(foreign key field)
    """
    period_number = models.IntegerField()
    employee_net_salary = models.FloatField()
    employee_gross_salary = models.FloatField()
    reimbursment_date = models.DateField()
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, null=True, blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, blank=True, null=True)


class Receipt(BaseModel):
    """
    This class(database table) defines the receipt for each
    payroll that is to be dispatched to each
    employee
    The fields belonging to this class are:
        - receipt_no(character field)
        - transaction_date(date field)
        - emp_id(foreign key field)
    """
    receipt_number = models.CharField(max_length=255)
    transaction_date = models.DateField()
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, null=True, blank=True)
