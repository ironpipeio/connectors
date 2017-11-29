#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 10:30:52 2017

@author: eckart
"""

import graphql
import stripe

stripe.api_key = "J7MAbERzeZP8gqBigFrSFi3vjBsd4Zof"

'''
stripe.Customer.retrieve("cus_BmoKWhEoRe37hZ")
stripe.Customer.list()

stripe.Product.retrieve("prod_95QBAuYWVs72DM")
stripe.Product.list()


customers = stripe.Customer.all(limit=3)
for customer in customers.auto_paging_iter():
    pass
  # Do something with customer

'''

# store in GQL file

type Customer {
        id: ID!
        created: Int!
        description: String
        email: String
}

type Query {
  # A feed of repository submissions
  listCustomers (
    # The sort order for the feed
    type: FeedType!,
    # The number of items to skip, for pagination
    offset: Int,
    # The number of items to fetch starting from the offset, for pagination
    limit: Int
  ): [Customer]
  
   # A single entry
  customer(
    id: ID!
  ): Customer

schema {
  query: Query
}



{
     customer(id: fdsfdsdf) {
         id
         created
         description
         email
     }
}


type Customer {
        id: ID!
        created: Int!
        description: String
        email: String
}

type Schema {
        }
query {
   customer(id:'fdsfds') {
       id
       created
       description
       email
   }
}

type Query {
  customer(id: ID!): Customer
  allCustomers(): [Customer]
}

type Product
def Query_me(request):
    return 'test'
}

def User_name(user) {
    return 'luke'

def resolve_users(args, context, info):
      // do something
      

resolvers = {
      'users': resolve_users
}

Then, in theory you can use graphql(schema, root_value=resolvers) to execute.




schema = graphql.build_ast_schema(graphql.parse(schema_text))

query_text = '''
    {
         me {
             name
         }
    }
'''

query_ast = graphql.parse(query_text)

errors = graphql.validate(schema, query_ast)


source = open('/path/to/graphql/schema/file')
ast = graphql.parse(source.read())
source.close()
schema = graphql.build_ast_schema(ast)

