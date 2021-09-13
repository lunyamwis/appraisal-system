import graphene
from graphql_extensions.auth.decorators import login_required

from ..helpers.permission_required import role_required, token_required
from ..helpers.validation_errors import error_dict
from ..helpers.constants import SUCCESS_ACTION
from .models import (
    Employee, Employer, Grade,
    Title, Course, Payroll, Department, SubDepartment
)
from ..authentication.models import User
from .validators.validate_input import EmployeeValidations
from app.api.helpers.validate_object_id import validate_object_id
from .object_types import (
    CourseInput, CourseType,
    DepartmentInput, DepartmentType,
    EmployeeInput, EmployeeType,
    EmployerInput, EmployerType,
    GradeInput, GradeType,
    DepartmentInput, DepartmentType,
    SubDepartmentInput,SubDepartmentType,
    PayrollInput, PayrollType,
    TitleInput, TitleType
)
from datetime import datetime


class CreateEmployee(graphene.Mutation):
    """
    This class handles the creation of the
    employee and saves the information to the db
    """
    # items that the mutation will return
    employee = graphene.Field(EmployeeType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        """
        this class handles the arguments to be
        passed in during the user creation
        """
        input = EmployeeInput(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        """
        the mutations for the employee creation. 
        Actual saving happens here.
        """
        error_msg = error_dict['admin_only'].format("create an employee")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        validator = EmployeeValidations()
        data = validator.validate_employee_registration_data(
            kwargs.get("input", '')
        )
        departments = data.pop("department", [])
        new_employee = Employee(**data)
        new_employee.save()
        if departments:
            for department in departments:
                department_ = Department.objects.get(id=department)
                new_employee.department.add(department_)
        return CreateEmployee(status="Success",
                              employee=new_employee,
                              message=SUCCESS_ACTION.format("Employee created"))


class UpdateEmployee(graphene.Mutation):
    """
    this class does the literal updating
    of employee details.
    """

    employee = graphene.Field(EmployeeType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        """
        arguments to be passed in during user
        creation.
        """
        input = EmployeeInput(required=True)
        id = graphene.String(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        error_msg = error_dict['admin_only'].format('update employee records')
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        id = kwargs.get('id', None)
        departments = kwargs['input'].pop('department', '')
        if kwargs['input']['employer_name']:
            kwargs['input']['employer_name'] = validate_object_id(
                kwargs['input']['employer_name'], Employer,
                "Employer")
        if kwargs['input']['job_title']:
            kwargs['input']['job_title'] = validate_object_id(
                kwargs['input']['job_title'], Title,
                "Title")
        employee_ = Employee.objects.get(id=id)
        for (key, value) in kwargs['input'].items():
            setattr(employee_, key, value)
        # import pdb; pdb.set_trace()
        employee_.save()


        if departments:
            for department in departments:
                department_ = Department.objects.get(id=department)
                employee_.department.add(department_)

        status = "Success"
        message = SUCCESS_ACTION.format("Employee record updated")
        return UpdateEmployee(status=status, employee=employee_, message=message)


class DeleteEmployee(graphene.Mutation):
    """
    This class handles the deletion or removal of employees
    """

    status = graphene.String()
    message = graphene.String()

    class Arguments:
        """
        This class handles the input during
        deletion of employees
        """
        id = graphene.List(graphene.String, required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(root, info, **kwargs):
        error_msg = error_dict['admin_only'].format("Remove an Employee")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        ids = kwargs.get('id', None)
        for id in ids:
            employee_ = validate_object_id(id, Employee, "Employee")
            employee_.delete()
        status = "Success"
        message = SUCCESS_ACTION.format("Employee has been removed")

        return DeleteEmployee(status=status, message=message)


class CreateEmployer(graphene.Mutation):
    """
    This class handles the creation of the
    employer and saves the information to the db
    """
    # items that the mutation will return
    employer = graphene.Field(EmployerType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        """
        this class handles the arguments to be
        passed in during the user creation
        """
        input = EmployerInput(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        """
        the mutations for the employee creation. 
        Actual saving happens here.
        """
        error_msg = error_dict['admin_only'].format("create an employer")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        validator = EmployeeValidations()
        data = validator.validate_employer_registration_data(
            kwargs.get("input", '')
        )
        new_employer = Employer(**data)
        new_employer.save()
        return CreateEmployer(status="Success",
                              employer=new_employer,
                              message=SUCCESS_ACTION.format("Employer created"))


class UpdateEmployer(graphene.Mutation):
    """
    this class does the literal updating
    of employer details.
    """

    employer = graphene.Field(EmployerType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        """
        arguments to be passed in during user
        creation.
        """
        input = EmployerInput(required=True)
        id = graphene.String(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        error_msg = error_dict['admin_only'].format('update employer records')
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        id = kwargs.get('id', None)
        if kwargs['input']['employer_details']:
            kwargs['input']['employer_details'] = validate_object_id(
                kwargs['input']['employer_details'], Employer,
                "Employer")
        employer_ = Employer.objects.get(id=id)
        for (key, value) in kwargs['input'].items():
            setattr(employer_, key, value)
        employer_.save()

        status = "Success"
        message = SUCCESS_ACTION.format("Employer records updated")
        return UpdateEmployer(status=status, employer=employer_, message=message)


class DeleteEmployer(graphene.Mutation):
    """
    This class handles the deletion or removal of employers
    """

    status = graphene.String()
    message = graphene.String()

    class Arguments:
        """
        This class handles the input during
        deletion of employers
        """
        id = graphene.List(graphene.String, required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(root, info, **kwargs):
        error_msg = error_dict['admin_only'].format("Remove an Employer")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        ids = kwargs.get('id', None)
        for id in ids:
            employer_ = validate_object_id(id, Employer, "Employer")
            employer_.delete()
        status = "Success"
        message = SUCCESS_ACTION.format("Employer has been removed")

        return DeleteEmployer(status=status, message=message)



class CreateCourse(graphene.Mutation):
    """
    This class handles the creation of the
    course and saves the information to the db
    """
    course = graphene.Field(CourseType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        """
        This class handles the input 
        during the creation of the course
        """
        input = CourseInput(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        """
        the mutations for the employee creation. 
        Actual saving happens here.
        """
        error_msg = error_dict['admin_only'].format("create a course")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        validator = EmployeeValidations()
        data = validator.validate_course_registration_data(
            kwargs.get("input", '')
        )
        new_course = Course(**data)
        new_course.save()
        return CreateCourse(status="Success",
                            course=new_course,
                            message=SUCCESS_ACTION.format("Course created"))


class UpdateCourse(graphene.Mutation):
    """
    this class does the literal updating
    of course details.
    """

    course = graphene.Field(CourseType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        """
        arguments to be passed in during user
        creation.
        """
        input = CourseInput(required=True)
        id = graphene.String(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        error_msg = error_dict['admin_only'].format('update course records')
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        id = kwargs.get('id', None)
        validator = EmployeeValidations()
        data = validator.validate_course_update_data(
            kwargs.get("input", ''), id
        )
        course_ = Course.objects.get(id=id)
        for (key, value) in data.items():
            setattr(course_, key, value)
        course_.save()

        status = "Success"
        message = SUCCESS_ACTION.format("Course records updated")
        return UpdateCourse(status=status, course=course_, message=message)


class DeleteCourse(graphene.Mutation):
    """
    This class handles the deletion or removal of courses
    """

    status = graphene.String()
    message = graphene.String()

    class Arguments:
        """
        This class handles the input during
        deletion of employers
        """
        id = graphene.List(graphene.String, required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(root, info, **kwargs):
        error_msg = error_dict['admin_only'].format("Remove an Employer")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        ids = kwargs.get('id', None)
        for id in ids:
            course_ = validate_object_id(id, Course, "Employer")
            course_.delete()
        status = "Success"
        message = SUCCESS_ACTION.format("Course has been removed")

        return DeleteCourse(status=status, message=message)


class CreatePayroll(graphene.Mutation):
    """
    This class handles the creation of the
    payroll and saves the information to the db
    """
    # items that the mutation will return
    payroll = graphene.Field(PayrollType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        """
        this class handles the arguments to be
        passed in during the user creation
        """
        input = PayrollInput(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        """
        the mutations for the payroll creation. 
        Actual saving happens here.
        """
        error_msg = error_dict['admin_only'].format("create a payroll")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        validator = EmployeeValidations()
        data = validator.validate_payroll_registration_data(
            kwargs.get("input", '')
        )
        new_payroll = Payroll(**data)
        new_payroll.save()
        return CreatePayroll(status="Success",
                             payroll=new_payroll,
                             message=SUCCESS_ACTION.format("Payroll created"))


class UpdatePayroll(graphene.Mutation):
    """
    this class does the literal updating
    of employer details.
    """

    payroll = graphene.Field(PayrollType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        """
        arguments to be passed in during user
        creation.
        """
        input = PayrollInput(required=True)
        id = graphene.String(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        error_msg = error_dict['admin_only'].format('update payroll records')
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        id = kwargs.get('id', None)
        validator = EmployeeValidations()
        data = validator.validate_payroll_update_data(
            kwargs.get("input", ''), id
        )
        payroll_ = Employer.objects.get(id=id)
        for (key, value) in data.items():
            setattr(payroll_, key, value)
        payroll_.save()

        status = "Success"
        message = SUCCESS_ACTION.format("Payroll records updated")
        return UpdatePayroll(status=status, payroll=payroll_, message=message)


class DeletePayroll(graphene.Mutation):
    """
    This class handles the deletion or removal of payroll
    """

    status = graphene.String()
    message = graphene.String()

    class Arguments:
        """
        This class handles the input during
        deletion of payroll
        """
        id = graphene.List(graphene.String, required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(root, info, **kwargs):
        error_msg = error_dict['admin_only'].format("Remove Payroll")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        ids = kwargs.get('id', None)
        for id in ids:
            payroll_ = validate_object_id(id, Payroll, "Payroll")
            payroll_.delete()
        status = "Success"
        message = SUCCESS_ACTION.format("Payroll has been removed")

        return DeletePayroll(status=status, message=message)


class CreateTitle(graphene.Mutation):
    """
    This class handles the creation of the
    title and saves the information to the db
    """
    # items that the mutation will return
    title = graphene.Field(TitleType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        """
        this class handles the arguments to be
        passed in during the user creation
        """
        input = TitleInput(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        """
        the mutations for the title creation. 
        Actual saving happens here.
        """
        error_msg = error_dict['admin_only'].format("create a title")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        validator = EmployeeValidations()
        data = validator.validate_title_registration_data(
            kwargs.get("input", '')
        )
        new_title = Title(**data)
        new_title.save()
        return CreateTitle(status="Success",
                           title=new_title,
                           message=SUCCESS_ACTION.format("Title created"))


class UpdateTitle(graphene.Mutation):
    """
    this class does the literal updating
    of title details.
    """

    title = graphene.Field(TitleType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        """
        arguments to be passed in during user
        creation.
        """
        input = TitleInput(required=True)
        id = graphene.String(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        error_msg = error_dict['admin_only'].format('update title records')
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        id = kwargs.get('id', None)
        validator = EmployeeValidations()
        data = validator.validate_title_update_data(
            kwargs.get("input", ''), id
        )
        title_ = Title.objects.get(id=id)
        for (key, value) in data.items():
            setattr(title_, key, value)
        title_.save()

        status = "Success"
        message = SUCCESS_ACTION.format("Title records updated")
        return UpdateTitle(status=status, title=title_, message=message)


class DeleteTitle(graphene.Mutation):
    """
    This class handles the deletion or removal of titles
    """

    status = graphene.String()
    message = graphene.String()

    class Arguments:
        """
        This class handles the input during
        deletion of title
        """
        id = graphene.List(graphene.String, required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(root, info, **kwargs):
        error_msg = error_dict['admin_only'].format("Remove Title")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        ids = kwargs.get('id', None)
        for id in ids:
            title_ = validate_object_id(id, Title, "Title")
            title_.delete()
        status = "Success"
        message = SUCCESS_ACTION.format("Title has been removed")

        return DeleteTitle(status=status, message=message)


class CreateDepartment(graphene.Mutation):
    """
    This class handles the creation of the
    department and saves the information to the db
    """
    # items that the mutation will return
    department = graphene.Field(DepartmentType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        """
        this class handles the arguments to be
        passed in during the user creation
        """
        input = DepartmentInput(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        """
        the mutations for the department creation. 
        Actual saving happens here.
        """
        error_msg = error_dict['admin_only'].format("create a department")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        validator = EmployeeValidations()
        data = validator.validate_department_registration_data(
            kwargs.get("input", '')
        )
        sub_departments = data.pop('sub_departments', [])
        new_department = Department(**data)
        new_department.save()
        for sub_department in sub_departments:
            sub_department.pop("amount", "")
            sub_department_ = SubDepartment(**sub_department)
            sub_department_.save()
            new_department.sub_departments.add(sub_department_)
        return CreateDepartment(status="Success",
                                department=new_department,
                                message=SUCCESS_ACTION.format("Department created"))


class UpdateDepartment(graphene.Mutation):
    """
    this class does the literal updating
    of department details.
    """

    department = graphene.Field(DepartmentType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        """
        arguments to be passed in during user
        creation.
        """
        input = DepartmentInput(required=True)
        id = graphene.String(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        error_msg = error_dict['admin_only'].format('update department records')
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        id = kwargs.get('id', None)
        department_ = Department.objects.get(id=id)
        sub_departments = kwargs['input'].pop('sub_departments', [])
        if kwargs['input']['pay_grade']:
            kwargs['input']['pay_grade'] = validate_object_id(
                kwargs['input']['pay_grade'], Grade,
                "Grade")
        for sub_dept in sub_departments:
            sub_department = SubDepartment(**sub_dept)
            sub_department.save()
            department_.sub_departments.add(sub_department)
        for (key, value) in kwargs['input'].items():
            setattr(department_, key, value)
        department_.save()

        status = "Success"
        message = SUCCESS_ACTION.format("Department records updated")
        return UpdateDepartment(status=status, department=department_, message=message)


class UpdateSubDepartment(graphene.Mutation):
    '''Handle update additional benefit details'''

    sub_department = graphene.Field(SubDepartmentType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        input = SubDepartmentInput(required=True)
        id = graphene.String(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(root, info, **kwargs):
        error_msg = error_dict['admin_only'].format("update an sub department")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        id = kwargs.get('id', None)
        validate_object_id(id, SubDepartment, "sub department")
        data = kwargs['input']
        add_ben = SubDepartment.objects.filter(id=id)
        add_ben.update(**data)

        sub_department = SubDepartment.objects.get(id=id)
        status = "Success"
        message = SUCCESS_ACTION.format("sub department updated")

        return UpdateSubDepartment(status=status,
                                   sub_department=sub_department,
                                   message=message)


class DeleteSubDepartment(graphene.Mutation):
    '''Handle update sub department details'''

    status = graphene.String()
    message = graphene.String()

    class Arguments:
        id = graphene.List(graphene.String, required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(root, info, **kwargs):
        error_msg = error_dict['admin_only'].format("delete an sub department")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        ids = kwargs.get('id', None)
        for id in ids:
            sub_det = validate_object_id(id, SubDepartment, "sub department")
            sub_dept.delete()
        status = "Success"
        message = SUCCESS_ACTION.format("sub department deleted")

        return DeleteSubDepartment(status=status,
                                   message=message)


class DeleteDepartment(graphene.Mutation):
    """
    This class handles the deletion or removal of department
    """

    status = graphene.String()
    message = graphene.String()

    class Arguments:
        """
        This class handles the input during
        deletion of payroll
        """
        id = graphene.List(graphene.String, required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(root, info, **kwargs):
        error_msg = error_dict['admin_only'].format("Remove Department")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        ids = kwargs.get('id', None)
        for id in ids:
            department_ = validate_object_id(id, Department, "Department")
            department_.delete()
        status = "Success"
        message = SUCCESS_ACTION.format("Department has been removed")

        return DeleteDepartment(status=status, message=message)


class CreateGrade(graphene.Mutation):
    """
    This class handles the creation of the
    grade and saves the information to the db
    """
    # items that the mutation will return
    grade = graphene.Field(GradeType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        """
        this class handles the arguments to be
        passed in during the user creation
        """
        input = GradeInput(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        """
        the mutations for the grade creation. 
        Actual saving happens here.
        """
        error_msg = error_dict['admin_only'].format("create a grade")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        validator = EmployeeValidations()
        data = validator.validate_grade_registration_data(
            kwargs.get("input", '')
        )
        new_grade = Grade(**data)
        new_grade.save()
        return CreateGrade(status="Success",
                           grade=new_grade,
                           message=SUCCESS_ACTION.format("Grade created"))


class UpdateGrade(graphene.Mutation):
    """
    this class does the literal updating
    of grade details.
    """

    grade = graphene.Field(GradeType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        """
        arguments to be passed in during user
        creation.
        """
        input = GradeInput(required=True)
        id = graphene.String(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(root, info, **kwargs):
        error_msg = error_dict['admin_only'].format('update grade records')
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        id = kwargs.get('id', None)
        validator = EmployeeValidations()
        data = validator.validate_grade_update_data(
            kwargs.get("input", ''), id
        )
        grade_ = Grade.objects.get(id=id)
        for (key, value) in data.items():
            setattr(grade_, key, value)
        grade_.save()

        status = "Success"
        message = SUCCESS_ACTION.format("Grade records updated")
        # import pdb; pdb.set_trace()
        return UpdateGrade(status=status, grade=grade_, message=message)


class DeleteGrade(graphene.Mutation):
    """
    This class handles the deletion or removal of grade
    """

    status = graphene.String()
    message = graphene.String()

    class Arguments:
        """
        This class handles the input during
        deletion of grade
        """
        id = graphene.List(graphene.String, required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(root, info, **kwargs):
        error_msg = error_dict['admin_only'].format("Remove Grade")
        role_required(info.context.user, ['admin', 'manager'], error_msg)
        ids = kwargs.get('id', None)
        for id in ids:
            grade_ = validate_object_id(id, Grade, "Grade")
            grade_.delete()
        status = "Success"
        message = SUCCESS_ACTION.format("Grade has been removed")

        return DeleteGrade(status=status, message=message)


class Mutation(graphene.ObjectType):
    create_employee = CreateEmployee.Field()
    update_employee = UpdateEmployee.Field()
    delete_employee = DeleteEmployee.Field()
    create_employer = CreateEmployer.Field()
    update_employer = UpdateEmployer.Field()
    delete_employer = DeleteEmployer.Field()
    create_course = CreateCourse.Field()
    update_course = UpdateCourse.Field()
    delete_course = DeleteCourse.Field()
    create_title = CreateTitle.Field()
    update_title = UpdateTitle.Field()
    delete_title = DeleteTitle.Field()
    create_payroll = CreatePayroll.Field()
    update_payroll = UpdatePayroll.Field()
    delete_payroll = DeletePayroll.Field()
    create_grade = CreateGrade.Field()
    update_grade = UpdateGrade.Field()
    delete_grade = DeleteGrade.Field()
    create_department = CreateDepartment.Field()
    update_department = UpdateDepartment.Field()
    delete_department = DeleteDepartment.Field()
    update_sub_department = UpdateSubDepartment.Field()
    delete_sub_department = DeleteSubDepartment.Field()