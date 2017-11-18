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
from addressbook.data.results import Result, build_result_error

"""
Functions to create data records.
"""
# TODO: add more meaningful results other than True and False for results and exceptions




def create_address(address):
    """Create an address.
    :param address: Class instance of Address() as parameter.
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)

        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("INSERT INTO address VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (None,
                   address.person_id,
                   address.address_line_1,
                   address.address_line_2,
                   address.po_box,
                   address.city,
                   address.state,
                   address.zip_code,
                   address.zip4,
                   address.postal_code,
                   address.status,
                   address.sequence_number,
                   address.type_id
                   ))
        new_row_id = c.lastrowid
        conn.commit()
        conn.close()
        return True, new_row_id
    except:
        return False, 0


def create_code(code):
    """Create a reference code (lookup code)
    :param code: Class instance of Code() as parameter.
    :return: Boolean indicating success of database action.
    """

    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("INSERT INTO codes VALUES (?,?, ?, ?)", (None, code.type_code,
                                                           code.type_description, code.reference_type))
        conn.commit()
        conn.close()
        return True
    except:
        return False


def create_comment(comment):
    """Create a comment.
    :param comment: Class instance of Comment() as parameter.
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("INSERT INTO comments VALUES (?, ?, ?)",
                  (comment.person_id,
                   comment.comment,
                   None
                   ))
        conn.commit()
        conn.close()
        return True
    except:
        return False


def create_person(person):
    """Create a person.
    :param person: Class instance of Person() as parameter.
    :return: Boolean indicating success of database action.
    """
    result = Result()
    try:
        with sqlite3.connect(settings.database_name) as conn:
            c = conn.cursor()
            c.execute("PRAGMA foreign_keys = ON")
            c.execute("INSERT INTO person VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (person.person_id,
                       person.first_name,
                       person.last_name,
                       person.middle_initial,
                       person.nick_name,
                       person.date_of_birth,
                       person.date_of_death
                       ))
            conn.commit()
            conn.close()
            result.message = "Success"
            result.value = True
        return result
    except sqlite3.DataError:
        return build_result_error("create_person", "DataError")
    except sqlite3.ProgrammingError:
        return build_result_error("create_person", "ProgrammingError")
    except sqlite3.IntegrityError:
        return build_result_error("create_person", "IntegrityError")
    except sqlite3.Error:
        return build_result_error("create_person", "Error")
    except Exception as Ex:
        return build_result_error("create_person", "SystemError")


def create_identification(identity):
    """Create an identification.
    :param identity: Class instance of Identity() as parameter.
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("INSERT INTO identification VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (identity.person_id,
                   identity.identification_number,
                   identity.type_code,
                   identity.issuing_authority,
                   identity.issuing_entity,
                   identity.record_location,
                   None
                   ))
        conn.commit()
        new_row_id = c.lastrowid
        conn.close()
        return True, new_row_id
    except:
        return False, 0


def create_phone_contact(phone):
    """Create a phone contact.
    :param phone: Class instance of Phone() as parameter.
    :return: Boolean indicating success of database action.
    """
    result = Result()
    try:
        with sqlite3.connect(settings.database_name) as conn:
            c = conn.cursor()
            c.execute("PRAGMA foreign_keys = ON")
            c.execute("INSERT INTO contact VALUES (?, ?)", (None, phone.person_id))
            new_row_id = c.lastrowid
            c.execute("INSERT INTO phone VALUES (?, ?, ?, ?, ?, ?);",
                      (c.lastrowid,
                       phone.type_code,
                       phone.sequence_number,
                       phone.area_code,
                       phone.exchange,
                       phone.trunk
                       ))
            conn.commit()
            # conn.close()
            result.message = "Success"
            result.value = new_row_id
            result.success = True
        return result
    except:
        result.message = "Failure"
        result.success = False
        result.error_status = True
        return result


def create_email_contact(email):
    """Create an email contact.
    :param email: Class instance of Email() as parameter.
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("INSERT INTO contact VALUES (?, ?)", (None, email.person_id))
        new_row_id = c.lastrowid
        # email.contact_id,
        c.execute("INSERT INTO email VALUES (?, ?, ?, ?)",
                  (c.lastrowid,
                   email.email_address,
                   email.sequence_number,
                   email.type_code
                   ))
        conn.commit()
        conn.close()
        return True, new_row_id
    except Exception as ex:
        # print(ex)
        return False, 0


def create_relation(relationship):
    """Create a relationship.
    :param relationship: Class instance of Relationship() as parameter.
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("INSERT INTO relationship VALUES (?, ?, ?, ?, ?)",
                  (relationship.person_id,
                   relationship.related_person_id,
                   relationship.relationship_type,
                   None,
                   relationship.related_person_relationship_type
                   ))
        new_row_id = c.lastrowid
        conn.commit()
        conn.close()
        return True, new_row_id
    except Exception as ex:
        yyy = ex
        return False, 0
