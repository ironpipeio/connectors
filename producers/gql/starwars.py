#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 17:41:18 2017

@author: eckart
"""

from collections import namedtuple

Human = namedtuple('Human', 'id name friends appearsIn homePlanet')

luke = Human(
    id='1000',
    name='Luke Skywalker',
    friends=['1002', '1003', '2000', '2001'],
    appearsIn=[4, 5, 6],
    homePlanet='Tatooine',
)

vader = Human(
    id='1001',
    name='Darth Vader',
    friends=['1004'],
    appearsIn=[4, 5, 6],
    homePlanet='Tatooine',
)

han = Human(
    id='1002',
    name='Han Solo',
    friends=['1000', '1003', '2001'],
    appearsIn=[4, 5, 6],
    homePlanet=None,
)

leia = Human(
    id='1003',
    name='Leia Organa',
    friends=['1000', '1002', '2000', '2001'],
    appearsIn=[4, 5, 6],
    homePlanet='Alderaan',
)

tarkin = Human(
    id='1004',
    name='Wilhuff Tarkin',
    friends=['1001'],
    appearsIn=[4],
    homePlanet=None,
)

humanData = {
    '1000': luke,
    '1001': vader,
    '1002': han,
    '1003': leia,
    '1004': tarkin,
}

Droid = namedtuple('Droid', 'id name friends appearsIn primaryFunction')

threepio = Droid(
    id='2000',
    name='C-3PO',
    friends=['1000', '1002', '1003', '2001'],
    appearsIn=[4, 5, 6],
    primaryFunction='Protocol',
)

artoo = Droid(
    id='2001',
    name='R2-D2',
    friends=['1000', '1002', '1003'],
    appearsIn=[4, 5, 6],
    primaryFunction='Astromech',
)

droidData = {
    '2000': threepio,
    '2001': artoo,
}


def getCharacter(id):
    return humanData.get(id) or droidData.get(id)


def getFriends(character):
    return map(getCharacter, character.friends)


def getHero(episode):
    if episode == 5:
        return luke
    return artoo


def getHuman(id):
    return humanData.get(id)


def getDroid(id):
    return droidData.get(id)


from graphql.type import (GraphQLArgument, GraphQLEnumType, GraphQLEnumValue,
                          GraphQLField, GraphQLInterfaceType, GraphQLList,
                          GraphQLNonNull, GraphQLObjectType, GraphQLSchema,
                          GraphQLString)

episodeEnum = GraphQLEnumType(
    'Episode',
    description='One of the films in the Star Wars Trilogy',
    values={
        'NEWHOPE': GraphQLEnumValue(
            4,
            description='Released in 1977.',
        ),
        'EMPIRE': GraphQLEnumValue(
            5,
            description='Released in 1980.',
        ),
        'JEDI': GraphQLEnumValue(
            6,
            description='Released in 1983.',
        )
    }
)

characterInterface = GraphQLInterfaceType(
    'Character',
    description='A character in the Star Wars Trilogy',
    fields=lambda: {
        'id': GraphQLField(
            GraphQLNonNull(GraphQLString),
            description='The id of the character.'
        ),
        'name': GraphQLField(
            GraphQLString,
            description='The name of the character.'
        ),
        'friends': GraphQLField(
            GraphQLList(characterInterface),
            description='The friends of the character, or an empty list if they have none.'
        ),
        'appearsIn': GraphQLField(
            GraphQLList(episodeEnum),
            description='Which movies they appear in.'
        ),
    },
    resolve_type=lambda character, info: humanType if getHuman(character.id) else droidType,
)

humanType = GraphQLObjectType(
    'Human',
    description='A humanoid creature in the Star Wars universe.',
    fields=lambda: {
        'id': GraphQLField(
            GraphQLNonNull(GraphQLString),
            description='The id of the human.',
        ),
        'name': GraphQLField(
            GraphQLString,
            description='The name of the human.',
        ),
        'friends': GraphQLField(
            GraphQLList(characterInterface),
            description='The friends of the human, or an empty list if they have none.',
            resolver=lambda human, *_: getFriends(human),
        ),
        'appearsIn': GraphQLField(
            GraphQLList(episodeEnum),
            description='Which movies they appear in.',
        ),
        'homePlanet': GraphQLField(
            GraphQLString,
            description='The home planet of the human, or null if unknown.',
        )
    },
    interfaces=[characterInterface]
)

droidType = GraphQLObjectType(
    'Droid',
    description='A mechanical creature in the Star Wars universe.',
    fields=lambda: {
        'id': GraphQLField(
            GraphQLNonNull(GraphQLString),
            description='The id of the droid.',
        ),
        'name': GraphQLField(
            GraphQLString,
            description='The name of the droid.',
        ),
        'friends': GraphQLField(
            GraphQLList(characterInterface),
            description='The friends of the droid, or an empty list if they have none.',
            resolver=lambda droid, info, **args: getFriends(droid),
        ),
        'appearsIn': GraphQLField(
            GraphQLList(episodeEnum),
            description='Which movies they appear in.',
        ),
        'primaryFunction': GraphQLField(
            GraphQLString,
            description='The primary function of the droid.',
        )
    },
    interfaces=[characterInterface]
)

queryType = GraphQLObjectType(
    'Query',
    fields=lambda: {
        'hero': GraphQLField(
            characterInterface,
            args={
                'episode': GraphQLArgument(
                    description='If omitted, returns the hero of the whole saga. If '
                                'provided, returns the hero of that particular episode.',
                    type=episodeEnum,
                )
            },
            resolver=lambda root, info, **args: getHero(args.get('episode')),
        ),
        'human': GraphQLField(
            humanType,
            args={
                'id': GraphQLArgument(
                    description='id of the human',
                    type=GraphQLNonNull(GraphQLString),
                )
            },
            resolver=lambda root, info, **args: getHuman(args['id']),
        ),
        'droid': GraphQLField(
            droidType,
            args={
                'id': GraphQLArgument(
                    description='id of the droid',
                    type=GraphQLNonNull(GraphQLString),
                )
            },
            resolver=lambda root, info, **args: getDroid(args['id']),
        ),
    }
)
StarWarsSchema = GraphQLSchema(query=queryType, types=[humanType, droidType])


from graphql import graphql
from graphql.error import format_error


def test_hero_name_query():
    query = '''
        query HeroNameQuery {
          hero {
            name
          }
        }
    '''
    expected = {
        'hero': {
            'name': 'R2-D2'
        }
    }
    result = graphql(StarWarsSchema, query)
    assert not result.errors
    assert result.data == expected


def test_hero_name_and_friends_query():
    query = '''
        query HeroNameAndFriendsQuery {
          hero {
            id
            name
            friends {
              name
            }
          }
        }
    '''
    expected = {
        'hero': {
            'id': '2001',
            'name': 'R2-D2',
            'friends': [
                {'name': 'Luke Skywalker'},
                {'name': 'Han Solo'},
                {'name': 'Leia Organa'},
            ]
        }
    }
    result = graphql(StarWarsSchema, query)
    assert not result.errors
    assert result.data == expected


def test_nested_query():
    query = '''
        query NestedQuery {
          hero {
            name
            friends {
              name
              appearsIn
              friends {
                name
              }
            }
          }
        }
    '''
    expected = {
        'hero': {
            'name': 'R2-D2',
            'friends': [
                {
                    'name': 'Luke Skywalker',
                    'appearsIn': ['NEWHOPE', 'EMPIRE', 'JEDI'],
                    'friends': [
                        {
                            'name': 'Han Solo',
                        },
                        {
                            'name': 'Leia Organa',
                        },
                        {
                            'name': 'C-3PO',
                        },
                        {
                            'name': 'R2-D2',
                        },
                    ]
                },
                {
                    'name': 'Han Solo',
                    'appearsIn': ['NEWHOPE', 'EMPIRE', 'JEDI'],
                    'friends': [
                        {
                            'name': 'Luke Skywalker',
                        },
                        {
                            'name': 'Leia Organa',
                        },
                        {
                            'name': 'R2-D2',
                        },
                    ]
                },
                {
                    'name': 'Leia Organa',
                    'appearsIn': ['NEWHOPE', 'EMPIRE', 'JEDI'],
                    'friends': [
                        {
                            'name': 'Luke Skywalker',
                        },
                        {
                            'name': 'Han Solo',
                        },
                        {
                            'name': 'C-3PO',
                        },
                        {
                            'name': 'R2-D2',
                        },
                    ]
                },
            ]
        }
    }
    result = graphql(StarWarsSchema, query)
    assert not result.errors
    assert result.data == expected


def test_fetch_luke_query():
    query = '''
        query FetchLukeQuery {
          human(id: "1000") {
            name
          }
        }
    '''
    expected = {
        'human': {
            'name': 'Luke Skywalker',
        }
    }
    result = graphql(StarWarsSchema, query)
    assert not result.errors
    assert result.data == expected


def test_fetch_some_id_query():
    query = '''
        query FetchSomeIDQuery($someId: String!) {
          human(id: $someId) {
            name
          }
        }
    '''
    params = {
        'someId': '1000',
    }
    expected = {
        'human': {
            'name': 'Luke Skywalker',
        }
    }
    result = graphql(StarWarsSchema, query, variable_values=params)
    assert not result.errors
    assert result.data == expected


def test_fetch_some_id_query2():
    query = '''
        query FetchSomeIDQuery($someId: String!) {
          human(id: $someId) {
            name
          }
        }
    '''
    params = {
        'someId': '1002',
    }
    expected = {
        'human': {
            'name': 'Han Solo',
        }
    }
    result = graphql(StarWarsSchema, query, variable_values=params)
    assert not result.errors
    assert result.data == expected


def test_invalid_id_query():
    query = '''
        query humanQuery($id: String!) {
          human(id: $id) {
            name
          }
        }
    '''
    params = {
        'id': 'not a valid id',
    }
    expected = {
        'human': None
    }
    result = graphql(StarWarsSchema, query, variable_values=params)
    assert not result.errors
    assert result.data == expected


def test_fetch_luke_aliased():
    query = '''
        query FetchLukeAliased {
          luke: human(id: "1000") {
            name
          }
        }
    '''
    expected = {
        'luke': {
            'name': 'Luke Skywalker',
        }
    }
    result = graphql(StarWarsSchema, query)
    assert not result.errors
    assert result.data == expected


def test_fetch_luke_and_leia_aliased():
    query = '''
        query FetchLukeAndLeiaAliased {
          luke: human(id: "1000") {
            name
          }
          leia: human(id: "1003") {
            name
          }
        }
    '''
    expected = {
        'luke': {
            'name': 'Luke Skywalker',
        },
        'leia': {
            'name': 'Leia Organa',
        }
    }
    result = graphql(StarWarsSchema, query)
    assert not result.errors
    assert result.data == expected


def test_duplicate_fields():
    query = '''
        query DuplicateFields {
          luke: human(id: "1000") {
            name
            homePlanet
          }
          leia: human(id: "1003") {
            name
            homePlanet
          }
        }
    '''
    expected = {
        'luke': {
            'name': 'Luke Skywalker',
            'homePlanet': 'Tatooine',
        },
        'leia': {
            'name': 'Leia Organa',
            'homePlanet': 'Alderaan',
        }
    }
    result = graphql(StarWarsSchema, query)
    assert not result.errors
    assert result.data == expected


def test_use_fragment():
    query = '''
        query UseFragment {
          luke: human(id: "1000") {
            ...HumanFragment
          }
          leia: human(id: "1003") {
            ...HumanFragment
          }
        }
        fragment HumanFragment on Human {
          name
          homePlanet
        }
    '''
    expected = {
        'luke': {
            'name': 'Luke Skywalker',
            'homePlanet': 'Tatooine',
        },
        'leia': {
            'name': 'Leia Organa',
            'homePlanet': 'Alderaan',
        }
    }
    result = graphql(StarWarsSchema, query)
    assert not result.errors
    assert result.data == expected


def test_check_type_of_r2():
    query = '''
        query CheckTypeOfR2 {
          hero {
            __typename
            name
          }
        }
    '''
    expected = {
        'hero': {
            '__typename': 'Droid',
            'name': 'R2-D2',
        }
    }
    result = graphql(StarWarsSchema, query)
    assert not result.errors
    assert result.data == expected


def test_check_type_of_luke():
    query = '''
        query CheckTypeOfLuke {
          hero(episode: EMPIRE) {
            __typename
            name
          }
        }
    '''
    expected = {
        'hero': {
            '__typename': 'Human',
            'name': 'Luke Skywalker',
        }
    }
    result = graphql(StarWarsSchema, query)
    assert not result.errors
    assert result.data == expected


def test_parse_error():
    query = '''
        qeury
    '''
    result = graphql(StarWarsSchema, query)
    assert result.invalid
    formatted_error = format_error(result.errors[0])
    assert formatted_error['locations'] == [{'column': 9, 'line': 2}]
    assert 'Syntax Error GraphQL request (2:9) Unexpected Name "qeury"' in formatted_error['message']
    assert result.data is None
    
#
#        
def main():   
    return test_check_type_of_luke()

if __name__ == '__main__':
    main()



