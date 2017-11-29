#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 18:29:19 2017

@author: eckart
"""

import graphene
import stripe

stripe.api_key = "J7MAbERzeZP8gqBigFrSFi3vjBsd4Zof"

class CustomerType(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    email = graphene.String()
    
class QueryType(graphene.ObjectType): 
    all_customers = graphene.List(CustomerType) 
    Customer = graphene.Field(CustomerType, id=graphene.ID())
    
    def resolve_all_customers(self, args, info):
        return Category.objects.all()
    
    def resolve_customer(self, args, info): 
        id = args.get('id')
        return Category.objects.get(pk=id)
    


class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    def resolve_hello(self, info, name):
        return 'Hello ' + name

schema = graphene.Schema(query=Query)

query = '{ hello }'

if __name__ == '__main__':
    result = schema.execute(query)
    print('errors', result.errors)
    print('data', result.data)
    



'''
class User(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    
class Customer(graphene.ObjectType):
     id =           graphene.ID(required=True)
     created =      graphene.Int()
     description =  graphene.String()
     email =        graphene.String()

class Query(graphene.ObjectType):
    me = graphene.Field(User)
    customer = graphene.Field(Customer)(id=graphene.String())

    def resolve_me(self, info):
        return info.context['user']
    
    def resolve_customer(self, info, id=None):
        if id is None:
            return [Customer(id='afdsdfs', created=10, description='hi', email='there'),
                    Customer(id='affdsfdsdfs', created=20, description='ho', email='hum')]
        else:
            return Customer(id=id, created=10, description='hi', email='there')
    
schema = graphene.Schema(query=Query)
'''
query = '''
    query foo {
      me {
        id
        name
      }
    }
'''

query2 = '''
    {
      customer(id: "1") {
        id
        created
        description
      }
    }
'''

query3 = '''
    {
      customer()
    }
'''

'''
def test_query():
    result = schema.execute(query, context_value={'user': User(id='1', name='Syrus')})
    assert not result.errors
    assert result.data == {
        'me': {
            'id': '1',
            'name': 'Syrus',
        }
    }


if __name__ == '__main__':
    result = schema.execute(query, context_value={'user': User(id='X', name='Console')})
    print(result.data['me'])
    
    
'''    
'''

class QueryType(graphene.ObjectType):
    name = 'Query'
    description = '...'
    
    hello = graphene.String()

    def resolve_hello(root, args, info):
        return 'world'
        
schema = graphene.Schema(
    query = QueryType
)

query_text = 
query {
     hello
}



class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    def resolve_hello(self, info, name):
        return 'Hello ' + name

schema = graphene.Schema(query=Query)

result = schema.execute('{ hello }')
print(result.data['hello']) # "Hello stranger"



class Customer(graphene.ObjectType):
     id =           graphene.ID(required=True)
     created =      graphene.Int()
     description =  graphene.String()
     email =        graphene.String()
    

class Query(graphene.ObjectType):
    
    def resolve_full_name(self, info):
        return '{} {}'.format(self.first_name, self.last_name)

    
            id: ID!
        created: Int!
        description: String
        email: String
}'''
    
