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

"""  Classes as objects.
Classes in this module represent a "Contact", a phone contact or a email contact.
"""


class Contact(object):
    """

    The main contact class used for email and phone contacts.

    Attributes:
        contact_id:         Contact identifier.
        person_id:          Person identifier for which the contact belongs.
        type_code:          The contact type.
        type_description:   The type long description.

    """
    def __init__(self):
        self.contact_id = None
        self.person_id = None
        self.type_code = None
        self.type_description = None


class Phone(Contact):
    """

        A standard USA phone number consisting of three digit area code, three digit exchange and four digit trunk.

        Attributes:
            phone_type_id:      Phone type identifier. Maps to code table in database.
            sequence_number:    Integer for ordering list of phone numbers.
            area_code:          Standard USA three digit area code of a phone number (first three numbers).
            exchange:           Standard three digit exchange of a phone number (second three numbers).
            trunk:              Standard four digit of phone number (last set of four digits).

        """
    def __init__(self):
        self.phone_type_id = None
        self.sequence_number = None
        self.area_code = None
        self.exchange = None
        self.trunk = None
        super().__init__()


class Email(Contact):
    """

        Email as contact inherited from Contact

        Attributes:
        email_type_id:      Type identifier as referenced in the database table codes.
        email_address:      Standard email address.
        sequence_number:    Integer for sorting list of email addresses.
    """
    def __init__(self):
        self.email_type_id = None
        self.email_address = None
        self.sequence_number = None
        super().__init__()
