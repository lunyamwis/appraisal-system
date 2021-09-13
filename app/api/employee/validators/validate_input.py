# Third party imports
import re

# Local imports
from django.core.exceptions import ObjectDoesNotExist
from graphql import GraphQLError

from ...helpers.constants import (
    EMPLOYEE_REQUIRED_FIELD, 
    EMPLOYER_REQUIRED_FIELD,
    COURSE_REQUIRED_FIELD,
    GENDER_OPTIONS
)
from ...helpers.validate_input import (check_email_validity,
                                       check_empty_fields,
                                       check_missing_fields)
from ...helpers.validation_errors import error_dict
from ...helpers.validate_object_id import validate_object_id
from ..models import (
    Course, Department, Employee,
    Employer, Payroll, Grade, Title
)


class EmployeeValidations:
    """
    Validations for the employment
    information
    """

    def validate_employee_registration_data(self, kwargs):
        """
        runs all employee data in one function
        args:
            kwargs(dict):request data
        returns:
            input_data(dict):validated data
        """
        check_missing_fields(kwargs, EMPLOYEE_REQUIRED_FIELD)
        input_data = {}
        input_data['first_name'] = kwargs.get('first_name', None)
        input_data['last_name'] = kwargs.get('last_name', None)
        check_empty_fields(data=input_data)
        input_data['employee_number'] = kwargs.get('employee_number',None)
        input_data['status'] = kwargs.get('status', None)
        input_data['gender'] = kwargs.get('gender', None)
        input_data['other_names'] = kwargs.get('other_names', None)
        input_data['email'] = kwargs.get('email', None)
        input_data['address'] = kwargs.get('address', None)
        input_data['phone_numbers'] = kwargs.get('phone_numbers', None)
        input_data['emergency_numbers'] = kwargs.get('emergency_numbers', None)
        input_data['date_of_birth'] = kwargs.get('date_of_birth', None)
        input_data['job_title'] = kwargs.get('job_title', None)
        input_data['employer_name'] = kwargs.get('employer_name', None)
        input_data['department'] = kwargs.get('department', None)
        input_data['hiring_date'] = kwargs.get('hiring_date', None)
        input_data['current_salary'] = kwargs.get('current_salary', None)
        input_data['starting_salary'] = kwargs.get('starting_salary', None)
        input_data['qualifications'] = kwargs.get('qualifications', None)
        input_data['completed_courses'] = kwargs.get('completed_courses', None)
        input_data['grade'] = kwargs.get('grade', None)
        input_data['rate_hour'] = kwargs.get('rate_hour', None)
        input_data['period'] = kwargs.get('period', None)
        input_data['per_period'] = kwargs.get('per_period', None)
        check_email_validity(
            input_data['email']) if input_data['email'] else ""

        if input_data['grade']:
            input_data['grade'] = validate_object_id(
                input_data['grade'], Grade,
                "Grade")

        if input_data['job_title']:
            input_data['job_title'] = validate_object_id(
                input_data['job_title'], Title,
                "Title")
        
        if input_data['employer_name']:
            input_data['employer_name'] = validate_object_id(
                input_data['employer_name'], Employer,
                "Employer")

        if input_data['completed_courses']:
            input_data['completed_courses'] = validate_object_id(
                input_data['completed_courses'], Course,
                "Course")

        return input_data

    def validate_employee_update_data(self, data, employee_id):
        """
        returns all employee update validations
        in one function
        args:
            data (dict): request data
            employee id (str):employee id
            user (obj): manager
        returns:
            input_data (dict):validated data
        """
        data_=validate_object_id(employee_id,Employee,"Employee")
        # data_ = check_empty_fields(data)
        # input_data={}
        # input_data['job_title'] = kwargs.get('job_title', None)
        # input_data['employer_name'] = kwargs.get('employer_name', None)
        # input_data['department'] = kwargs.get('department', None)
        # input_data['completed_courses'] = kwargs.get('completed_courses', None)
        # input_data['grade'] = kwargs.get('grade', None)
        # input_data = {k: v for k, v in input_data.items() if v}
        # import pdb; pdb.set_trace()
        return data_


    def validate_employer_registration_data(self,kwargs):
        """
        runs all employer data in one function
        args:
            kwargs(dict):request data
        returns:
            input_data(dict):validated data
        """
        check_missing_fields(kwargs, EMPLOYER_REQUIRED_FIELD)
        input_data = {}
        input_data['business_name'] = kwargs.get('business_name',None)
        input_data['phone_numbers'] = kwargs.get('phone_numbers',None)
        input_data['website_link'] = kwargs.get('website_link',None)
        input_data['address'] = kwargs.get('address',None)
        input_data['contact_name'] = kwargs.get('contact_name',None)
        input_data['contact_phone_number'] = kwargs.get('contact_phone_number',None)
        input_data['contact_role'] = kwargs.get('contact_role',None)
        input_data['employer_details'] = kwargs.get('employer_details',None)
        input_data['location'] = kwargs.get('location',None)
        input_data['industry'] = kwargs.get('industry',None)
        input_data['size'] = kwargs.get('size',None)
        return input_data


    def validate_employer_update_data(self, data, employer_id):
        """
        returns all employee update validations
        in one function
        args:
            data (dict): request data
            employee id (str):employee id
            user (obj): manager
        returns:
            input_data (dict):validated data
        """
        validate_object_id(employer_id,Employer,"Employer")
        data_ = check_empty_fields(data)

        return data_
    
    def validate_course_registration_data(self,kwargs):
        """
        runs all course data in one function
        args:
            kwargs(dict):request data
        returns:
            input_data(dict):validated data
        """
        check_missing_fields(kwargs, COURSE_REQUIRED_FIELD)
        input_data = {}
        input_data['course_name'] = kwargs.get('course_name',None)
        input_data['course_level'] = kwargs.get('course_level',None)
        return input_data


    def validate_course_update_data(self, data, course_id):
        """
        returns all course update validations
        in one function
        args:
            data (dict): request data
            course id (str):course id
            user (obj): manager
        returns:
            input_data (dict):validated data
        """
        validate_object_id(course_id,Course,"Course")
        data_ = check_empty_fields(data)

        return data_
    
    def validate_payroll_registration_data(self,kwargs):
        """
        runs all course data in one function
        args:
            kwargs(dict):request data
        returns:
            input_data(dict):validated data
        """
        input_data = {}
        input_data['period_number']=kwargs.get('period_number',None)
        input_data['employee_net_salary']=kwargs.get('employee_net_salary',None)
        input_data['employee_gross_salary']=kwargs.get('employee_gross_salary',None)
        input_data['reimbursment_date']=kwargs.get('reimbursment_date',None)
        input_data['employee']=kwargs.get('employee',None)
        input_data['grade']=kwargs.get('grade',None)
        return input_data


    def validate_payroll_update_data(self, data, course_id):
        """
        returns all course update validations
        in one function
        args:
            data (dict): request data
            course id (str):course id
            user (obj): manager
        returns:
            input_data (dict):validated data
        """
        validate_object_id(course_id,Payroll,"Payroll")
        data_ = check_empty_fields(data)

        return data_
    
    def validate_title_registration_data(self,kwargs):
        """
        runs all course data in one function
        args:
            kwargs(dict):request data
        returns:
            input_data(dict):validated data
        """
        input_data = {}
        input_data['title_name'] = kwargs.get('title_name',None)
        return input_data


    def validate_title_update_data(self, data, course_id):
        """
        returns all course update validations
        in one function
        args:
            data (dict): request data
            course id (str):course id
            user (obj): manager
        returns:
            input_data (dict):validated data
        """
        validate_object_id(course_id,Title,"Title")
        data_ = check_empty_fields(data)

        return data_
    
    def validate_department_registration_data(self,kwargs):
        """
        runs all course data in one function
        args:
            kwargs(dict):request data
        returns:
            input_data(dict):validated data
        """
        
        input_data = {}
        input_data['department_name']=kwargs.get('department_name',None)
        input_data['sub_departments'] = kwargs.get('sub_departments',[])
        input_data['pay_grade']=kwargs.get('pay_grade',None)
        if input_data['pay_grade']:
            input_data['pay_grade'] = validate_object_id(
                input_data['pay_grade'], Grade,
                "Grade")
        return input_data


    def validate_department_update_data(self, data, department_id):
        """
        returns all course update validations
        in one function
        args:
            data (dict): request data
            course id (str):course id
            user (obj): manager
        returns:
            input_data (dict):validated data
        """
        validate_object_id(department_id,Department,"Department")
        if data['pay_grade']:
            data['pay_grade'] = validate_object_id(
                data['pay_grade'], Grade,
                "Grade")
        data_ = check_empty_fields(data)
    
    

        return data_

    def validate_grade_registration_data(self,kwargs):
        """
        runs all course data in one function
        args:
            kwargs(dict):request data
        returns:
            input_data(dict):validated data
        """
        input_data = {}
        input_data['grade_name']=kwargs.get('grade_name',None)
        input_data['grade_basic']=kwargs.get('grade_basic',None)
        input_data['grade_da']=kwargs.get('grade_da',None)
        input_data['grade_ta']=kwargs.get('grade_ta',None)
        input_data['grade_bonus']=kwargs.get('grade_bonus',None)
        input_data['grade_pf']=kwargs.get('grade_pf',None)
        return input_data


    def validate_grade_update_data(self, data, grade_id):
        """
        returns all course update validations
        in one function
        args:
            data (dict): request data
            course id (str):course id
            user (obj): manager
        returns:
            input_data (dict):validated data
        """
        validate_object_id(grade_id,Grade,"Grade")
        data_ = check_empty_fields(data)

        return data_