import graphene
from django_filters import OrderingFilter
from graphene.types.generic import GenericScalar
from graphene_django.types import DjangoObjectType

from .models import (
    Employer,
    Employee,
    Department,
    Grade,
    Title,
    Course,
    Payroll,
    SubDepartment
)


class EmployerType(DjangoObjectType):
    """
    This class creates a graphql type for
    the Employer model
    """
    class Meta:
        """
        This class defines the fields
        to be serialized in the user model
        """
        model = Employer


class EmployeeType(DjangoObjectType):
    """
    This class creates a graphql type
    for the Employee model
    class Employee()
    """
    status =graphene.String()
    
    class Meta:
        """
        This class defines the fields
        to be serialized in the user model
        """
        model = Employee


class DepartmentType(DjangoObjectType):
    """
    This class creates a graphql type
    for the Department model
    """
    class Meta:
        """
        This class defines the fields
        to be serialized in the user model
        """
        model = Department


class SubDepartmentType(DjangoObjectType):
    """
    This class creates a graphql type
    for the Department model
    """
    class Meta:
        """
        This class defines the fields
        to be serialized in the user model
        """
        model = SubDepartment


class GradeType(DjangoObjectType):
    """
    This class creates a graphql type
    for the grade model
    """
    class Meta:
        """
        This class defines the fields
        to be serialized in the user model
        """
        model = Grade


class CourseType(DjangoObjectType):
    """
    This class creates a graphql type
    for the course model
    """
    course_level = graphene.String()
    class Meta:
        """
        This class defines the fields
        to be serialized in the course model
        """
        model = Course



class TitleType(DjangoObjectType):
    """
    This class creates a graphql type
    for the title model
    """
    class Meta:
        """
        This class defines the fields
        to be serialized in the user model
        """
        model = Title


class PayrollType(DjangoObjectType):
    """
    This class creates a graphql type
    for the payroll model
    """
    class Meta:
        """
        This class defines the fields
        to be serialized in the user model
        """
        model = Payroll




class EmployerInput(graphene.InputObjectType):
    """
    This class creates input object types for
    the Employee model
    """

    business_name = graphene.String()
    phone_numbers = graphene.String()
    website_link = graphene.String()
    address = graphene.String()
    contact_name = graphene.String()
    contact_phone_number = graphene.String()
    contact_role = graphene.String()
    employer_details = graphene.String()
    location = graphene.String()
    industry = graphene.String()
    size = graphene.String()

class SubDepartmentInput(graphene.InputObjectType):
    """
    This class creates input object types for
    the Employee model
    """
    name = graphene.String()

class DepartmentInput(graphene.InputObjectType):
    """
    This class creates input object types for
    the Employee model
    """
    department_name = graphene.String()
    pay_grade = graphene.String()
    sub_departments = graphene.List(SubDepartmentInput)


class TitleInput(graphene.InputObjectType):
    """
    This class creates input object types for
    the Employee model
    """
    title_name = graphene.String()


class CourseInput(graphene.InputObjectType):
    """
    This class creates input object types for
    the Employee model
    """
    course_name = graphene.String()
    course_level = graphene.String()


class PayrollInput(graphene.InputObjectType):
    """
    This class creates input object types for
    the Employee model
    """
    period_number = graphene.Int()
    employee_net_salary = graphene.Float()
    employee_gross_salary = graphene.Float()
    reimbursment_date = graphene.Date()
    employee = graphene.String()
    grade = graphene.String()


class GradeInput(graphene.InputObjectType):
    """
    This class creates input object types for
    the Employee model
    """
    grade_name = graphene.String()
    grade_basic = graphene.String()
    grade_da = graphene.String()
    grade_ta = graphene.String()
    grade_bonus = graphene.Float()
    grade_pf = graphene.String()


class EmployeePaginatedType(graphene.ObjectType):
    """
    Employee pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    items = graphene.List(EmployeeType)


class EmployerPaginatedType(graphene.ObjectType):
    """
    Employer pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    items = graphene.List(EmployerType)


class PayrollPaginatedType(graphene.ObjectType):
    """
    Payroll pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    items = graphene.List(PayrollType)


class CoursePaginatedType(graphene.ObjectType):
    """
    Course pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    items = graphene.List(CourseType)

class TitlePaginatedType(graphene.ObjectType):
    """
    Title pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    items = graphene.List(TitleType)

class DepartmentPaginatedType(graphene.ObjectType):
    """
    Course pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    items = graphene.List(DepartmentType)

class GradePaginatedType(graphene.ObjectType):
    """
    Grade pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    items = graphene.List(GradeType)


class EmployeeInput(graphene.InputObjectType):
    """
    This class creates input object types for
    the Employee model
    """

    first_name = graphene.String()
    employee_number = graphene.String()
    last_name = graphene.String()
    other_names = graphene.String()
    email = graphene.String()
    address = graphene.String()
    phone_numbers = graphene.String()
    emergency_numbers = graphene.String()
    date_of_birth = graphene.Date()
    job_title = graphene.String()
    employer_name = graphene.String()
    department = graphene.List(graphene.String)
    hiring_date = graphene.Date()
    current_salary = graphene.Float()
    starting_salary = graphene.Float()
    qualifications = graphene.String()
    completed_courses = graphene.String()
    rate_hour = graphene.Float()
    period = graphene.String()
    per_period = graphene.Float()
    grade = graphene.String()
    status = graphene.String()
    gender = graphene.String()
