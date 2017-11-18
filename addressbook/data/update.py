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
from addressbook.data.results import Result

# TODO: add more meaningful results other than True and False for results and exceptions


def update_address(address):
    """Updates address record for the specified address instance.
    :param address: Class instance of Address()
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("UPDATE address SET personid=?, addressline1=?, addressline2=?, pobox=?, city=?, state=?,"
                  " zipcode=?, zip4=?, postalcode=?, status=?, typeid=?, sequenceno=? WHERE addressid=?",
                  (address.person_id,
                   address.address_line_1,
                   address.address_line_2,
                   address.po_box,
                   address.city,
                   address.state,
                   address.zip_code,
                   address.zip4,
                   address.postal_code,
                   address.status,
                   address.type_id,
                   address.sequence_number,
                   address.address_id))

        conn.commit()
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()
        return True
    except:
        return False


def update_code(code):
    """Updates a code record for the specified code instance.
    :param code: Class instance of Code()
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("UPDATE codes SET typecode=?, typedescription=?, referencetype=? WHERE typeid=?",
                  (code.type_code,
                   code.type_description,
                   code.reference_type,
                   code.type_id
                   ))
        conn.commit()
        conn.close()
        return True
    except:
        return False


def update_comment(comment):
    """Updates a comment for the specified comment instance.
    :param comment: Class instance of Comment()
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("UPDATE comments SET comment=? WHERE commentid=? AND personid=?",
                  (comment.comment,
                   comment.comment_id,
                   comment.person_id
                   ))
        conn.commit()
        conn.close()
        return True
    except:
        return False


def update_person(person):
    """Updates person record for the specified person instance.
    :param person: Class instance of person.
    :return: Boolean indicating success of database action.
    """
    result = Result()
    try:
        with sqlite3.connect(settings.database_name) as conn:
            c = conn.cursor()
            c.execute("PRAGMA foreign_keys = ON")
            c.execute("UPDATE person SET firstname=?, lastname=?, "
                      "middleinitial=?, nickname=?, dateofbirth=?, dateofdeath=? WHERE personid=?",
                      (person.first_name,
                       person.last_name,
                       person.middle_initial,
                       person.nick_name,
                       person.date_of_birth,
                       person.date_of_death,
                       person.person_id
                       ))
            conn.commit()
            # conn.close()
            result.success = True
            result.message = "Success"
        return result
    except sqlite3.DataError:
        result.error_status = True
        result.message = "SQLite Data Error"
        result.value = False
        return result
    except sqlite3.ProgrammingError:
        result.error_status = True
        result.message = "SQLite Programming Error"
        result.value = False
        return result
    except sqlite3.IntegrityError:
        result.error_status = True
        result.message = "SQLite Data Integrity Error"
        result.value = False
        return result
    except sqlite3.Error:
        result.error_status = True
        result.message = "SQLite Base Error"
        result.value = False
        return result
    except Exception as Ex:
        result.error_status = True
        result.message = Ex.__cause__
        result.value = False
        return result



def update_identification(identity):
    """Updates identity record for the specified identity instance.
    :param identity: Class instance of Identity()
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("UPDATE identification SET identificationnumber=?, identificationtypeid=?, "
                  "issuingauthority=?, issuingentity=?, recordlocation=? "
                  "WHERE personid=? AND identificationid=?",
                  (identity.identification_number,
                   identity.type_code,
                   identity.issuing_authority,
                   identity.issuing_entity,
                   identity.record_location,
                   identity.person_id,
                   identity.identification_id
                   ))
        conn.commit()
        conn.close()
        return True
    except:
        return False


def update_phone_contact(phone):
    """Updates phone contact for the specified phone instance.
    :param phone: Class instance of Phone()
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("UPDATE phone SET typeid=?, sequenceno=?, areacode=?, exchange=?, trunk=? WHERE contactid=?;",
                  (
                   phone.type_code,
                   phone.sequence_number,
                   phone.area_code,
                   phone.exchange,
                   phone.trunk,
                   phone.contact_id
                   ))
        conn.commit()
        conn.close()
        return True
    except:
        return False


def update_email_contact(email):
    """Updates email contact for the specified email instance.
    :param email: Class instance of Email()
    :return: Boolean indicating success of database action.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("UPDATE email SET emailaddress=?, sequenceno=?, typeid=? WHERE contactid=?",
                  (email.email_address,
                   email.sequence_number,
                   email.type_code,
                   email.contact_id
                   ))
        conn.commit()
        conn.close()
        return True
    except:
        return False


def update_relation(relationship):
    """Updates relationship for the specified relationship instance.
    :param relationship: Class instance of Relationship().
    :return: Boolean indicating success of database action.
    """
    conn = sqlite3.connect(settings.database_name)
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON")
    c.execute("UPDATE relationship SET related_personid=?, relationshiptype=? WHERE personid=? AND relationshipid=?",
              (relationship.related_person_id,
               relationship.relationship_type,
               relationship.person_id,
               relationship.relationship_id
               ))
    conn.commit()
    conn.close()
