import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, engine, Department as DepartmentModel, Employee as EmployeeModel, BDResult
from sqlalchemy import text

import hashlib


def getmd5hash(str2hash):
    # encoding GeeksforGeeks using encode()
    # then sending to md5()
    result = hashlib.md5(str2hash.encode())
    return result.hexdigest()


class Department(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node,)


class Employee(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node,)


class Person(graphene.ObjectType):
    ''' We can set the schema description for an Object Type here on a docstring '''

    class Meta:
        model = BDResult
        interfaces = (relay.Node,)
        description = "Hi, this is Yash, old employee leaving a backdoor"

    first_name = graphene.String()
    last_name = graphene.String()
    full_name = graphene.String()

    def resolve(self):
        return None

    def resolve_first_name(parent, info):
        return "Yash"

    def resolve_last_name(parent, info):
        return "Sodha"

    def resolve_full_name(parent, info):
        return f"{parent.first_name} {parent.last_name}"


class Backdoor(graphene.ObjectType):
    class Meta:
        model = BDResult
        description = "Hi, this is Yash, old employee leaving a backdoor"


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
    all_employees = SQLAlchemyConnectionField(Employee)
    # Disable sorting over this field
    all_departments = SQLAlchemyConnectionField(Department, sort=None)

    backdoor = graphene.String(description="Hi, this is Yash, an old employee leaving a backdoor.\n"
                                           + "Get employee information from the employee table. \n"
                                           + "Just specify the ID of the employee in the `id` argument. \n"
                                           + "Along with hash of the employee id(just for added security you know)"
                                           + "For example, id:2, hash: c81e728d9d4c2f636f067f89cc14862c",
                               id=graphene.String(), hash=graphene.String())

    # person = graphene.Field(Person, q=graphene.String(), hash=graphene.String())

    def resolve_person(self, info, **kwargs):
        return Person("yash", "sodha")

    def resolve_backdoor(self, info, **args):
        q = args.get("id")
        hash = args.get("hash")

        print(q)
        if hash.lower() != getmd5hash(q).lower():
            raise Exception("Hash doesn't match")
        res = engine.execute(text('SELECT name FROM `employee` WHERE id=\'' + q + '\''))

        return res.fetchone()[0]


schema = graphene.Schema(query=Query)
