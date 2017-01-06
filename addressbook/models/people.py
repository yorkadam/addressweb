# The MIT License (MIT)
#
# Copyright (c) 2016 Adam York
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Classes as objects.
Classes in this module represent a person, relationship, and comment.
"""


class Person(object):
    """

    A person class which represents a person in the address book.

    Attributes:
        person_id:      Person identifier (row identifier)
        first_name:     First name.
        last_name:      Last Name.
        middle_initial. Middle Initial.
        nick_name:      Nick Name.
        date_of_birth:  Date of birth in YYYY-MM-DD format.
        date_of_death:  Date of death in YYYY-MM-DD format.
        relatives:      A list of assigned relationship(s) to another person.
        identities:     A list of associated identities (identification).
        addresses:      A list of address.
        contacts:       A list of contacts.
        comments:       A list of comments.

    """
    def __init__(self):
        self.person_id = None
        self.first_name = None
        self.last_name = None
        self.middle_initial = None
        self.nick_name = None
        self.date_of_birth = None
        self.date_of_death = None
        self.relatives = []
        self.identities = []
        self.addresses = []
        self.contacts = []
        self.comments = []


class Relationship(object):
    """

    A person relationship.

    Attributes:

        person_id:          The person identifier for which this relationship is assigned.
        related_person_id:  The person identifier for which this person is related.
        relationship_type:  The type of relationship between two people as designated by the assigned relationship.
        relationship_id:    The identifier for the relationship (a row identifier)
        relationship_type_description:  The description of the relationship type.
        related_person_relationship_type: The related person's relationship type.
        person = Person(). Inherited from Person

    """

    def __init__(self):
        self.person_id = None
        self.related_person_id = None
        self.relationship_type = None
        self.relationship_id = None
        self.relationship_type_description = None
        self.related_person_relationship_type = None
        self.person = Person()  # TODO: reactor Relationship and Relatiohship2 into a properly inherited class


class Relationship2(Person):
    """

    A person relationship.

    Attributes:

        person_id:          The person identifier for which this relationship is assigned.
        related_person_id:  The person identifier for which this person is related.
        relationship_type:  The type of relationship between two people as designated by the assigned relationship.
        relationship_id:    The identifier for the relationship (a row identifier)
        relationship_type_description:  The description of the relationship type.
        related_person_relationship_type: The related person's relationship type.
        person = Person(). Inherited from Person

    """

    def __init__(self):
        self.person_id = None
        self.related_person_id = None
        self.relationship_type = None
        self.relationship_id = None
        self.relationship_type_description = None
        self.related_person_relationship_type = None


class Comment(object):
    """

    Person comment class.

    Attributes:
        person_id: Person identifier for which the comment belongs.
        comment: Comment content.
        comment_id: Comment identifier (row identifier)

    """
    def __init__(self):
        self.person_id = None
        self.comment = None
        self.comment_id = None
