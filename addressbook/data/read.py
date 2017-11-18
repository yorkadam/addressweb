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
from addressbook.models.addresses import *
from addressbook.models.codes import *
from addressbook.models.contacts import *
from addressbook.models.identities import *
from addressbook.models.people import *
import re

# TODO: add more meaningful results other than True and False for results and exceptions

relationship_query = """SELECT p.personid, relations.related_personid, relations.key, relations.value, p.firstname,
                     p.lastname, p.middleinitial,
                     p.nickname, p.dateofbirth, p.dateofdeath, relations.relationshiptype,
                     relations.relationshipid
                     FROM (
                            SELECT
                              r.personid         AS personid,
                              r.relationshiptype,
                              r.relationshipid,
                              r.related_personid AS related_personid
                              , c.key, c.value
                            FROM relationship AS r
                              JOIN relationshipmap AS c ON c.relationshiptype = r.relationshiptype
                            UNION
                            SELECT
                              r.related_personid AS personid,
                              r.related_person_relationshiptype,
                              r.relationshipid,
                              r.personid  AS related_personid,
                               c.key,
                              c.value

                            FROM relationship AS r
                              JOIN relationshipmap AS c ON c.relationshiptype = r.related_person_relationshiptype
                          ) relations
                     JOIN person p on p.personid = relations.personid
                     WHERE relations.related_personid = ?"""


def read_address(address):
    """ Reads an address from the database for the specified address.
    :param address: Class instance of Address()
    :return: List[] of Address
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("SELECT * FROM address WHERE addressid=?", (address.address_id,))

        address_list = []
        for row in c:
            _address = Address()
            _address.address_id = row["addressid"]
            _address.person_id = row["personid"]
            _address.address_line_1 = row["addressline1"]
            _address.address_line_2 = row["addressline2"]
            _address.po_box = row["pobox"]
            _address.city = row["city"]
            _address.state = row["state"]
            _address.zip_code = row["zipcode"]
            _address.zip4 = row["zip4"]
            _address.postal_code = row["postalcode"]
            _address.status = row["status"]
            _address.address_type = row["addresstype"]
            _address.sequence_number = row["sequenceno"]
            address_list.append(_address)
        conn.close()
        return address_list
    except:
        return []


def read_addresses(person_id):
    """Reads address for the specified person identifier (row identifier).
    :param person_id: Person identifier (row identifier).
    :return: List of Address()
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("SELECT a.addressid, a.personid, a.addressline1, a.addressline2, a.pobox, a.city, a.state, "
                  "a.zipcode, a.zip4, a.postalcode, a.status, a.typeid, a.sequenceno, c.typecode, c.typedescription "
                  "FROM Address a "
                  "JOIN codes c on c.typeid = a.typeid WHERE personid=? ORDER BY a.sequenceno ASC", (person_id,))

        address_list = []
        for row in c:
            _address = Address()
            _address.address_id = row["addressid"]
            _address.person_id = row["personid"]
            _address.address_line_1 = row["addressline1"]
            _address.address_line_2 = row["addressline2"]
            _address.po_box = row["pobox"]
            _address.city = row["city"]
            _address.state = row["state"]
            _address.zip_code = row["zipcode"]
            _address.zip4 = row["zip4"]
            _address.postal_code = row["postalcode"]
            _address.status = row["status"]
            _address.type_id = row["typeid"]
            _address.sequence_number = row["sequenceno"]
            _address.type_code = row["typecode"]
            _address.type_description = row["typedescription"]
            address_list.append(_address)
        conn.close()
        return address_list
    except:
        return []


def read_all_codes(code):
    """Reads all codes.
    :param code: Class instance of Code()
    :return: List of Codes()
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("SELECT * FROM codes", code.type_id)
        code_list = []
        for row in c:
            _code = Code()
            _code.type_id = row["typeid"]
            _code.type_code = row["typecode"]
            _code.type_description = row["typedescription"]
            _code.reference_type = row["referencetype"]
            code_list.append(_code)
        conn.close()
        return code_list
    except:
        return []


def read_lookup_code_by_reference(reference_type):
    """Reads codes for the specified reference type.
    :param reference_type: The reference type.
    :return: List of Codes()
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("SELECT * FROM codes WHERE referencetype=?", (reference_type,))
        code_list = []
        # _code = None
        for row in c:
            _code = Code()
            _code.type_id = row["typeid"]
            _code.type_code = row["typecode"]
            _code.type_description = row["typedescription"]
            _code.reference_type = row["referencetype"]
            code_list.append(_code)
        conn.close()
        return code_list
    except:
        return []


def read_comment(person_id):
    """Reads a comment for the specified person identifier (row identifier).
    :param person_id: Person identifier (row identifier).
    :return: List of Comment()
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("SELECT * FROM comments WHERE personid=?", (person_id,))
        comment_list = []
        for row in c:
            _comment = Comment()
            _comment.person_id = row["personid"]
            _comment.comment = row["comment"]
            _comment.comment_id = row["commentid"]
            comment_list.append(_comment)
        conn.close()
        return comment_list
    except:
        return []


def read_person(person_id):
    """Reads person for specified person identifier (row identifier)
    :param person_id: Person identifier (row identifier)
    :return: Instance of Person() or None
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("SELECT * FROM person WHERE personid =?", (person_id,))
        _person = None
        for row in c:
            _person = Person()
            _person.person_id = row["personid"]
            _person.first_name = row["firstname"]
            _person.last_name = row["lastname"]
            _person.middle_initial = row["middleinitial"]
            _person.nick_name = row["nickname"]
            _person.date_of_birth = row["dateofbirth"]
            _person.date_of_death = row["dateofdeath"]
        conn.close()
        return _person
    except:
        return None


def is_person_identifier_used(person_id):
    """Indicates if the person identifier has been previously used in the database.
    :param person_id: Person identifier to be checked.
    :return: Boolean, True = Used, False = Not Used.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("SELECT personid FROM person WHERE personid =?", (person_id,))
        person_identifier = ""
        is_used = True
        for row in c:
            person_identifier = row["personid"]
        conn.close()
        if len(person_identifier) == 0:
            is_used = False
        if len(person_identifier) > 0:
            is_used = True
        return is_used
    except:
        return False


def read_people():
    """Reads all people from the database.
    :return: List of Person().
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("SELECT * FROM person LIMIT {0};".format(settings.search_result_row_limit))
        p = []
        for row in c:
            _person = Person()
            _person.person_id = row["personid"]
            _person.first_name = row["firstname"]
            _person.last_name = row["lastname"]
            _person.middle_initial = row["middleinitial"]
            _person.nick_name = row["nickname"]
            _person.date_of_birth = row["dateofbirth"]
            _person.date_of_death = row["dateofdeath"]
            p.append(_person)
        conn.close()
        return p
    except:
        return []


def read_identification(person_id):
    """Reads all identities for the specified person identifier (row identifier)
    :param person_id: Person identifier (row identifier)
    :return: List of Identity()
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("SELECT i.personid, i.identificationnumber, i.identificationtypeid, i.issuingauthority, "
                  "i.issuingentity, i.recordlocation, i.identificationid, c.typecode, c.typedescription, c.typeid "
                  "FROM identification i "
                  "JOIN codes c on c.typeid = i.identificationtypeid WHERE personid =?;", (person_id,))

        identity_list = []
        for row in c:
            _identity = Identity()
            _identity.person_id = row["personid"]
            _identity.identification_number = row["identificationnumber"]
            _identity.identification_type_id = row["identificationtypeid"]
            _identity.issuing_authority = row["issuingauthority"]
            _identity.issuing_entity = row["issuingentity"]
            _identity.record_location = row["recordlocation"]
            _identity.identification_id = row["identificationid"]
            _identity.type_code = row["typecode"]
            _identity.type_code_id = row["typeid"]
            _identity.type_description = row["typedescription"]
            identity_list.append(_identity)
        conn.close()
        return identity_list
    except:
        return []


def read_phone_contacts(person_id):
    """Read all phone contacts for the specified person identifier.
    :param person_id: Person identifier (row identifier).
    :return: List of Phone()
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("SELECT c.personid, c.contactid,  p.typeid, p.sequenceno, p.areacode, p.exchange, p.trunk, "
                  "co.typecode, co.typedescription "
                  "FROM contact AS c "
                  "JOIN phone AS p ON c.contactid = p.contactid "
                  "JOIN codes co on co.typeid = p.typeid "
                  "WHERE c.personid = ? ORDER BY p.sequenceno ASC;", (person_id,))

        phone_list = []
        for row in c:
            _phone = Phone()
            _phone.person_id = row["personid"]
            _phone.contact_id = row["contactid"]
            _phone.phone_type_id = row["typeid"]
            _phone.sequence_number = row["sequenceno"]
            _phone.area_code = row["areacode"]
            _phone.exchange = row["exchange"]
            _phone.trunk = row["trunk"]
            _phone.type_code = row["typecode"]
            _phone.phone_type_id = row["typeid"]
            _phone.type_description = row["typedescription"]
            phone_list.append(_phone)
        conn.close()
        return phone_list
    except:
        return []


def read_email_contacts(person_id):
    """Reads all email contacts for the specified person identifier (row identifier)
    :param person_id: Person identifier (row identifier).
    :return: List of Email()
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")

        c.execute("SELECT c.personid, c.contactid, e.emailaddress, e.sequenceno, "
                  "co.typeid, co.typecode, co.typedescription "
                  "FROM contact AS c "
                  "JOIN email AS e ON e.contactid = c.contactid "
                  "JOIN codes co on co.typeid = e.typeid WHERE c.personid =? ORDER BY e.sequenceno ASC;", (person_id,))

        email_list = []
        for row in c:
            _email = Email()
            _email.person_id = row["personid"]
            _email.contact_id = row["contactid"]
            _email.email_address = row["emailaddress"]
            _email.sequence_number = row["sequenceno"]
            _email.email_type_id = row["typeid"]
            _email.type_code = row["typecode"]
            _email.type_description = row["typedescription"]
            email_list.append(_email)
        conn.close()
        return email_list
    except:
        return []


def read_relationships(person_id):
    """Reads all relationships for the specified person identifier (row identifier).
    :param person_id: Person identifier (row identifier).
    :return: List of Relationship()
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute(relationship_query, (person_id,))  # note a tuple is needed as a parameter value for SQLITE

        relation_list = []
        for row in c:
            _relation = Relationship()
            _relation.person_id = row["personid"]
            _relation.person.first_name = row["firstname"]
            _relation.person.last_name = row["lastname"]
            _relation.person.middle_initial = row["middleinitial"]
            _relation.related_person_id = row["related_personid"]
            _relation.relationship_id = row["relationshipid"]
            _relation.relationship_type = row["relationshiptype"]
            _relation.relationship_type_description = row["key"]
            relation_list.append(_relation)
        conn.close()
        return relation_list
    except:
        return []


def read_relationship_map():
    """Reads the mapping for relationships between people.
    :return: Dictionary of tuples.
    """
    try:
        conn = sqlite3.connect(settings.database_name)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("SELECT * FROM relationshipmap")
        relation_dictionary = {}
        for row in c:
            relation_dictionary[row["key"]] = (row["key"], row["value"], row["relationshiptype"])
        conn.close()
        return relation_dictionary
    except:
        return {}


def search_people_1(search_type, search_value):
    """Reads (searches) person records for the specified search type and equal search value.
    :param search_type: Type varies based on search options.
    :param search_value: The value to search for.
    :return: List of Person()
    """
    try:
        # Search Types:
        # First Name, Last Name, Address 1, Address 2, City, State, Zip Code, Phone, Email, Identification
        # COLLATE NOCASE
        # column place holder variables are needed for coalesce to work right.
        first_name = None
        last_name = None
        address_line_1 = None
        address_line_2 = None
        city = None
        state = None
        zip_code = None

        conn = sqlite3.connect(settings.database_name)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")

        # with name search we use coalesce and search for only one value at a time,
        # which ever is passed first name or last name. This means our WHERE clause effectively becomes one of two cases
        # Case 1: WHERE firstname = search_value AND lastname = lastname
        # Case 1: WHERE firstname = firstname AND lastname = search_value
        # This pattern is repeated for the remaining searches where more than one parameter is expected.
        if search_type in {"First Name", "Last Name"}:
            if search_type == "First Name":
                first_name = search_value
            if search_type == "Last Name":
                last_name = search_value

            c.execute("SELECT DISTINCT p.personid, p.firstname, p.lastname, p.middleinitial, p.nickname, "
                      "p.dateofbirth, p.dateofdeath "
                      "FROM person p "
                      "WHERE  p.firstname = coalesce(?, p.firstname) COLLATE NOCASE "
                      "AND p.lastname = coalesce(?, p.lastname) COLLATE NOCASE;", (first_name, last_name))

        if search_type in {"Address 1", "Address 2", "City", "State", "Zip Code"}:
            if search_type == "Address 1":
                address_line_1 = search_value
            if search_type == "Address 2":
                address_line_2 = search_value
            if search_type == "City":
                city = search_value
            if search_type == "State":
                state = search_value
            if search_type == "Zip Code":
                zip_code = search_value

            c.execute("SELECT DISTINCT p.personid, p.firstname, p.lastname, p.middleinitial, p.nickname,   "
                      "p.dateofbirth, p.dateofdeath "
                      "FROM person p "
                      "LEFT JOIN address a on a.personid = p.personid "
                      "WHERE a.addressline1 = coalesce(?, a.addressline1) COLLATE NOCASE "
                      "AND   a.addressline2 = coalesce(?, a.addressline2) COLLATE NOCASE "
                      "AND  a.city = coalesce(?, a.city) COLLATE NOCASE "
                      "AND  a.state = coalesce(?, a.state) COLLATE NOCASE "
                      "AND a.zipcode = coalesce(?, a.zipcode) COLLATE NOCASE;", (address_line_1, address_line_2,
                                                                                 city, state, zip_code))

        if search_type == "Phone":
            c.execute("SELECT DISTINCT p.personid, p.firstname, p.lastname,   p.middleinitial, p.nickname, "
                      "p.dateofbirth, p.dateofdeath "
                      "FROM person p "
                      "JOIN contact c on c.personid = p.personid "
                      "JOIN phone  ph on ph.contactid = c.contactid "
                      "WHERE ph.areacode || ph.exchange || ph.trunk = ?;", (re.sub("[^0-9]", "", search_value),))

        if search_type == "Email":
            c.execute("SELECT DISTINCT p.personid, p.firstname, p.lastname,   p.middleinitial, p.nickname,"
                      "p.dateofbirth, p.dateofdeath "
                      "FROM person p "
                      "JOIN contact c on c.personid = p.personid "
                      "JOIN email  e on e.contactid = c.contactid "
                      "WHERE e.emailaddress = ? COLLATE NOCASE;", (search_value,))

        if search_type == "Identification":
            c.execute("SELECT DISTINCT p.personid, p.firstname, p.lastname, p.middleinitial, p.nickname, "
                      "p.dateofbirth, p.dateofdeath "
                      "FROM person p "
                      "JOIN identification i on i.personid = p.personid "
                      "WHERE i.identificationnumber = ? COLLATE NOCASE;", (search_value,))

        p = []
        if search_type == "All":
            p = read_people()
        else:
            for row in c:
                _person = Person()
                _person.person_id = row["personid"]
                _person.first_name = row["firstname"]
                _person.last_name = row["lastname"]
                _person.middle_initial = row["middleinitial"]
                _person.nick_name = row["nickname"]
                _person.date_of_birth = row["dateofbirth"]
                _person.date_of_death = row["dateofdeath"]
                p.append(_person)
            conn.close()
        return p
    except:
        return []


def search_people_2(search_type, search_value):
    """Reads (searches) person records for the specified search type which contains search value.
    :param search_type: Type varies based on search options.
    :param search_value: The value to search for.
    :return: List of Person()
    """
    try:
        # Search Types:
        # First Name, Last Name, Address 1, Address 2, City, State, Zip Code, Phone, Email, Identification
        query_string_name =\
            "SELECT DISTINCT p.personid, p.firstname, p.lastname, p.middleinitial, p.nickname, "\
            "p.dateofbirth, p.dateofdeath "\
            "FROM person p "\
            "WHERE  {0} LIKE ? COLLATE NOCASE;"
        query_string_address =\
            "SELECT DISTINCT p.personid, p.firstname, p.lastname, p.middleinitial, p.nickname,   "\
            "p.dateofbirth, p.dateofdeath "\
            "FROM person p "\
            "LEFT JOIN address a on a.personid = p.personid "\
            "WHERE {0} LIKE ? COLLATE NOCASE "

        conn = sqlite3.connect(settings.database_name)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        final_query = ""
        if search_type in {"First Name", "Last Name"}:
            if search_type == "First Name":
                final_query = query_string_name.format("p.firstname")
            if search_type == "Last Name":
                final_query = query_string_name.format("p.lastname")
            c.execute(final_query, ("%"+search_value+"%",))

        if search_type in {"Address 1", "Address 2", "City", "State", "Zip Code"}:
            if search_type == "Address 1":
                final_query = query_string_address.format("a.addressline1")
                c.execute(final_query, ("%"+search_value+"%",))
            if search_type == "Address 2":
                final_query = query_string_address.format("a.addressline2")
                c.execute(final_query, ("%"+search_value+"%",))
            if search_type == "City":
                final_query = query_string_address.format("a.city")
                c.execute(final_query, ("%"+search_value+"%",))
            if search_type == "State":
                final_query = query_string_address.format("a.state")
                c.execute(final_query, ("%"+search_value+"%",))
            if search_type == "Zip Code":
                final_query = query_string_address.format("a.zipcode")
                c.execute(final_query, ("%"+search_value+"%",))

        if search_type == "Phone":
            c.execute("SELECT DISTINCT p.personid, p.firstname, p.lastname,   p.middleinitial, p.nickname, "
                      "p.dateofbirth, p.dateofdeath "
                      "FROM person p "
                      "JOIN contact c on c.personid = p.personid "
                      "JOIN phone  ph on ph.contactid = c.contactid "
                      "WHERE ph.areacode || ph.exchange || ph.trunk LIKE ?;", ("%"+search_value+"%",))

        if search_type == "Email":
            c.execute("SELECT DISTINCT p.personid, p.firstname, p.lastname,   p.middleinitial, p.nickname,"
                      "p.dateofbirth, p.dateofdeath "
                      "FROM person p "
                      "JOIN contact c on c.personid = p.personid "
                      "JOIN email  e on e.contactid = c.contactid "
                      "WHERE e.emailaddress LIKE ? COLLATE NOCASE;", ("%"+search_value+"%",))

        if search_type == "Identification":
            c.execute("SELECT DISTINCT p.personid, p.firstname, p.lastname, p.middleinitial, p.nickname, "
                      "p.dateofbirth, p.dateofdeath "
                      "FROM person p "
                      "JOIN identification i on i.personid = p.personid "
                      "WHERE i.identificationnumber LIKE ? COLLATE NOCASE;", ("%"+search_value+"%",))

        p = []
        if search_type == "All":
            p = read_people()
        else:
            for row in c:
                _person = Person()
                _person.person_id = row["personid"]
                _person.first_name = row["firstname"]
                _person.last_name = row["lastname"]
                _person.middle_initial = row["middleinitial"]
                _person.nick_name = row["nickname"]
                _person.date_of_birth = row["dateofbirth"]
                _person.date_of_death = row["dateofdeath"]
                p.append(_person)
            conn.close()
        return p
    except Exception as exc:
        aexc = exc
        return []
