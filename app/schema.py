import graphene

from app.api.authentication.mutations import Mutation as auth_mutation
from app.api.authentication.query import Query as user_query
from app.api.employee.mutations import Mutation as employee_mutation
from app.api.employee.query import Query as employee_query


class Query(user_query, employee_query, graphene.ObjectType):
    """
    This class will inherit from multiple Queries
    as we begin to add more apps to our project
    """
    pass


class Mutation(auth_mutation, employee_mutation, graphene.ObjectType):
    """
    This class will inherit from multiple Queries
    as we begin to add more apps to our project
    """
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
