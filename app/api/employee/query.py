import graphene
from django.db.models import Q
from graphene_django.types import ObjectType
from graphql_extensions.auth.decorators import login_required
from graphene.types.generic import GenericScalar

from app.api.helpers.pagination_helper import pagination_helper
from app.api.helpers.permission_required import token_required
from app.api.helpers.validate_object_id import validate_object_id
from .models import (
    Employee, Employer,
    Course,Payroll,Grade,
    Title,Department
)
from .object_types import (
    EmployeeType, EmployeePaginatedType,
    EmployerType, EmployerPaginatedType,
    CourseType,CoursePaginatedType,
    PayrollType,PayrollPaginatedType,
    TitleType,TitlePaginatedType,
    DepartmentType,DepartmentPaginatedType,
    GradeType,GradePaginatedType
)

from .helpers.employee_helpers import get_default_status


class Query(ObjectType):
    status = GenericScalar()
    employee = graphene.Field(EmployeeType, id=graphene.String())
    employees = graphene.Field(
        EmployeePaginatedType,
        page=graphene.Int(),
        search=graphene.String(),
        limit=graphene.Int()
    )
    employer = graphene.Field(EmployerType, id=graphene.String())
    employers = graphene.Field(
        EmployerPaginatedType,
        page=graphene.Int(),
        search=graphene.String(),
        limit=graphene.Int()
    )
    course = graphene.Field(CourseType, id=graphene.String())
    courses = graphene.Field(
        CoursePaginatedType,
        page=graphene.Int(),
        search=graphene.String(),
        limit=graphene.Int()
    )
    department = graphene.Field(DepartmentType, id=graphene.String())
    departments = graphene.Field(
        DepartmentPaginatedType,
        page=graphene.Int(),
        search=graphene.String(),
        limit=graphene.Int()
    )
    title = graphene.Field(TitleType, id=graphene.String())
    titles = graphene.Field(
        TitlePaginatedType,
        page=graphene.Int(),
        search=graphene.String(),
        limit=graphene.Int()
    )
    grade = graphene.Field(GradeType, id=graphene.String())
    grades = graphene.Field(
        GradePaginatedType,
        page=graphene.Int(),
        search=graphene.String(),
        limit=graphene.Int()
    )
    payroll = graphene.Field(PayrollType, id=graphene.String())
    payrolls = graphene.Field(
        PayrollPaginatedType,
        page=graphene.Int(),
        search=graphene.String(),
        limit=graphene.Int()
    )


    @token_required
    @login_required
    def resolve_status(self, info, **kwargs):
        return get_default_status()

    @token_required
    @login_required
    def resolve_employee(self, info, **kwargs):
        id = kwargs.get('id', None)
        return validate_object_id(id, Employee, "Employee")

    @token_required
    @login_required
    def resolve_employees(self, info, search=None, **kwargs):
        page = kwargs.get('page', 1)
        limit = kwargs.get('limit', 10)
        if search:
            filter = (
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(other_names__icontains=search) |
                Q(email__icontains=search) |
                Q(address__icontains=search) |
                Q(phone_numbers__icontains=search) |
                Q(emergency_numbers__icontains=search) |
                Q(date_of_birth__icontains=search) |
                Q(job_title__title_name__icontains=search) |
                Q(employer_name__employer_details__username__icontains=search) |
                Q(employer_name__employer_details__first_name__icontains=search) |
                Q(employer_name__employer_details__last_name__icontains=search) |
                Q(employer_name__business_name__icontains=search) |
                Q(department__department_name__icontains=search) |
                Q(hiring_date__icontains=search) |
                Q(qualifications__icontains=search) |
                Q(completed_courses__course_name__icontains=search) |
                Q(grade__grade_name__icontains=search)
            )
            employees = Employee.objects.filter(
                filter).all().order_by('-created_at')
        else:
            employees = Employee.objects.filter().all().order_by('-created_at')

        return pagination_helper(employees, page, limit, EmployeePaginatedType)

    @token_required
    @login_required
    def resolve_employer(self, info, **kwargs):
        id = kwargs.get('id', None)
        return validate_object_id(id, Employer, "Employer")

    @token_required
    @login_required
    def resolve_employers(self, info, search=None, **kwargs):
        page = kwargs.get('page', 1)
        limit = kwargs.get('limit', 10)
        if search:
            filter = (
                Q(business_name__icontains=search) |
                Q(website_link__icontains=search) |
                Q(contact_phone_number__icontains=search) |
                Q(contact_name__icontains=search) |
                Q(contact_role__icontains=search) |
                Q(address__icontains=search) |
                Q(phone_numbers__icontains=search) |
                Q(employer_details__user__username__icontains=search) |
                Q(employer_details__user__first_name__icontains=search) |
                Q(employer_details__user__last_name__icontains=search) |
                Q(location__icontains=search) |
                Q(industry__icontains=search) |
                Q(size__icontains=search) 
            )
            employers = Employer.objects.filter(
                filter).all().order_by('-created_at')
        else:
            employers = Employer.objects.filter().all().order_by('-created_at')

        return pagination_helper(employers, page, limit, EmployerPaginatedType)

    @token_required
    @login_required
    def resolve_course(self, info, **kwargs):
        id = kwargs.get('id', None)
        return validate_object_id(id, Course, "Course")

    @token_required
    @login_required
    def resolve_courses(self, info, search=None, **kwargs):
        page = kwargs.get('page',None)
        limit = kwargs.get('limit',None)

        if search:
            filter = (
                Q(course_name__icontains=search) |
                Q(course_level__icontains=search) 
            )
            courses = Course.objects.filter(
                filter).all().order_by('-created_at')
        else:
            courses = Course.objects.filter().all().order_by('-created_at')

        return pagination_helper(courses, page, limit, CoursePaginatedType)

    @token_required
    @login_required
    def resolve_department(self, info, **kwargs):
        id = kwargs.get('id', None)
        return validate_object_id(id, Department, "Department")

    @token_required
    @login_required
    def resolve_departments(self, info, search=None, **kwargs):
        page = kwargs.get('page',None)
        limit = kwargs.get('limit',None)

        if search:
            filter = (
                Q(department_name__icontains=search) |
                Q(pay_grade__grade_name__icontains=search) 
            )
            courses = Department.objects.filter(
                filter).all().order_by('-created_at')
        else:
            courses = Department.objects.filter().all().order_by('-created_at')

        return pagination_helper(courses, page, limit, DepartmentPaginatedType)

    @token_required
    @login_required
    def resolve_title(self, info, **kwargs):
        id = kwargs.get('id', None)
        return validate_object_id(id, Title, "Title")

    @token_required
    @login_required
    def resolve_titles(self, info, search=None, **kwargs):
        page = kwargs.get('page',None)
        limit = kwargs.get('limit',None)

        if search:
            filter = (
                Q(title_name__icontains=search) 
            )
            titles = Title.objects.filter(
                filter).all().order_by('-created_at')
        else:
            titles = Title.objects.filter().all().order_by('-created_at')

        return pagination_helper(titles, page, limit, TitlePaginatedType)

    @token_required
    @login_required
    def resolve_payroll(self, info, **kwargs):
        id = kwargs.get('id', None)
        return validate_object_id(id, Payroll, "Payroll")

    @token_required
    @login_required
    def resolve_payrolls(self, info, search=None, **kwargs):
        page = kwargs.get('page',None)
        limit = kwargs.get('limit',None)

        if search:
            filter = (
                Q(period_number__icontains=search)|
                Q(employee_net_salary__icontains=search)|
                Q(employee_gross_salary__icontains=search)|
                Q(reimbursment_date__icontains=search)|
                Q(employee__first_name__icontains=search)|
                Q(grade__grade__name__icontains=search)
            )
            payrolls = Payroll.objects.filter(
                filter).all().order_by('-created_at')
        else:
            payrolls = Payroll.objects.filter().all().order_by('-created_at')

        return pagination_helper(payrolls, page, limit, PayrollPaginatedType)

    @token_required
    @login_required
    def resolve_grade(self, info, **kwargs):
        id = kwargs.get('id', None)
        return validate_object_id(id, Grade, "Grade")

    @token_required
    @login_required
    def resolve_grades(self, info, search=None, **kwargs):
        page = kwargs.get('page',None)
        limit = kwargs.get('limit',None)

        if search:
            filter = (
                Q(grade_name__icontains=search)|
                Q(grade_basic__icontains=search)|
                Q(grade_da__icontains=search)|
                Q(grade_ta__icontains=search)|
                Q(grade_bonus__icontains=search)|
                Q(grade_pf__icontains=search)
            )
            grades = Grade.objects.filter(
                filter).all().order_by('-created_at')
        else:
            grades = Grade.objects.filter().all().order_by('-created_at')

        return pagination_helper(grades, page, limit, GradePaginatedType)

    