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

import sqlite3

from addressbook import settings


# NOTES: Just a reminder that parametrization of ? needs a tuple for the expression provided to the where clause.
# Example "WHERE personid = ?;", (person_id,))  notice TWO (2) element tuple with one blank signified by the trailing
# comma.  Also, conn.commit() is necessary or the statement will not work for edit and delete.

# TODO: add more meaningful results other than True and False for results and exceptions

def delete_address(address_id):
    """Deletes 1 address.
    :param address_id: The address identifier (database row identifier).
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("DELETE FROM address WHERE addressid=?;", (address_id,))
        conn.commit()
        conn.close()
        return True
    except:
        return False


def delete_all_addresses():
    """Deletes ALL addresses from the database.
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("DELETE FROM address")
        conn.commit()
        conn.close()
        return True
    except:
        return False


def delete_all_lookup_codes():
    """Deletes all lookup codes from the database.
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("DELETE FROM codes")
        conn.commit()
        conn.close()
        return True
    except:
        return False


def delete_lookup_code(code_type_id):
    """Deletes a single lookup code (reference code).
    :param code_type_id: Deletes type code for the specified type identifier (row identifier)
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("DELETE FROM codes WHERE typeid=?", code_type_id)
        conn.commit()
        conn.close()
        return True
    except:
        return False


def delete_comment(person_id, comment_id):
    """Deletes a comment for the specified person identifier and comment identifier (row identifiers)
    :param person_id: Person identifier.
    :param comment_id: Comment identifier.
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("DELETE FROM comments WHERE personid=? AND commentid=?", (person_id, comment_id,))
        conn.commit()
        conn.close()
        return True
    except:
        return False


def delete_all_person_comments(person_id):
    """Delete all comments for the specified person identifier.
    :param person_id: Person identifier (row identifier)
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("DELETE FROM comments WHERE personid=?", person_id)
        conn.commit()
        conn.close()
        return True
    except:
        return False


def delete_all_comments():
    """Deletes all comments regardless of person.
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("DELETE FROM comments")
        conn.commit()
        conn.close()
        return True
    except:
        return False


def delete_person(person_id):
    """Deletes a person for the given person identifier.
    :param person_id: Person identifier (row identifier).
    :return: Boolean indicating success of the database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        # WARNING DELETES ALL RELATED RECORDS COMPLETELY DUE TO CASCADE DELETE
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("DELETE FROM person "
                  "WHERE personid = ?;", (person_id,))
        conn.commit()
        conn.close()
        return True
    except:
        return False


def delete_all_people():
    """Deletes all person records from the database.
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("DELETE FROM person")
        conn.commit()
        conn.close()
        return True
    except:
        return False


def delete_all_person_addresses(person_id):
    """Deletes all address for the specified person identifier.
    :param person_id: Person identifier (row identifier).
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("DELETE FROM address WHERE personid = ?;", (person_id,))
        conn.commit()
        conn.close()
        return True
    except:
        return False


def delete_identification(identification_id):
    """Deletes an identity for the specified identity identifier (row identifier)
    :param identification_id: Identity identifier (row identifier)
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("DELETE FROM identification WHERE identificationid=?", (identification_id,))
        conn.commit()
        conn.close()
        return True
    except:
        return False


def delete_all_person_identification(person_id):
    """Deletes all identity records for the specified person identifier (row identifier).
    :param person_id: Person identifier (row identifier).
    :return: Boolean indicating success of the database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("DELETE FROM identification WHERE personid=?", person_id)
        conn.commit()
        conn.close()
        return True
    except:
        return False


def delete_all_identification():
    """Deletes all identification records from the database.
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("DELETE FROM identification")
        conn.commit()
        conn.close()
        return True
    except:
        return False


def delete_contact(contact_id):
    """ Deletes a contact for the specified contact identifier (row identifier).
    :param contact_id: Contact identifier (row identifier).
    :return: Boolean indicating success of database action.
    """

    # for both email and phone we don't need two separate since we are using cascade on delete
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("DELETE FROM contact WHERE contactid = ?;", (contact_id,))
        conn.commit()
        conn.close()
        return True
    except:
        return False


def delete_all_person_contacts(person_id):
    """Deletes all contacts for the specified person identifier (row identifier).
    :param person_id: Person identifier (row identifier).
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("DELETE FROM contact WHERE personid = ?", person_id)
        conn.commit()
        conn.close()
        return True
    except:
        return False


def delete_all_contacts():
    """Deletes all contacts from the database.
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("DELETE FROM contact")
        conn.commit()
        conn.close()
        return True
    except:
        return False


def delete_relationship(relationship_id):
    """Deletes a relationship for the specified relationship identifier (row identifier).
    :param relationship_id: Relationship identifier (row identifier).
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("DELETE FROM relationship WHERE relationshipid=?", (relationship_id,))
        conn.commit()
        conn.close()
        return True
    except:
        return False


def delete_all_person_relationships(person_id):
    """Deletes all relationships for the specified person identifier (row identifier).
    :param person_id: Person identifier (row identifier).
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("DELETE FROM relationship WHERE personid=?", person_id)
        conn.commit()
        conn.close()
        return True
    except:
        return False


def delete_all_relationships():
    """Delete all relationships in the database.
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("DELETE FROM relationship")
        conn.commit()
        conn.close()
        return True
    except:
        return False
