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

"""Classes as objects for this module.
Used to represent a street address for one or more people.

"""

# TODO: Either implement GPS or remove if feature will not be implemented.

class Address(object):
    """

    Address class for standard mailing addresses

    Attributes:
        address_id:         The address identifier for the database row.
        person_id:          The person identifier for the database row.
        address_line_1:     Address Line 1. The first line of a standard address.
        address_line_2:     Address Line 2. The second line of a standard address.
        po_box:             P.O. BOX (Post office box) A USA Federal box number for the USA Postal Mail System.
        city:               The city name for the address.
        state:              State, a 2 character abbreviation as specified by the USPS for postal mailing to addresses.
        zip_code:           Standard USPS zip code.
        zip4:               Standard USPS zip-4 code.
        postal_code:        Postal code for addresses not using standard USPS zip codes.
        status:             Mostly unused. Future implementation.
        type_id:            The address type identifier. Maps to table "codes" in database.
        sequence_number:    Sequence number. Used to order a list of addresses.
        type_code:          An abbreviation of the type code description. Maps to table "codes" in database.
        type_description:   A long description of address types. Maps to table "codes" in database.

    """

    def __init__(self):
        self.address_id = None
        self.person_id = None
        self.address_line_1 = None
        self.address_line_2 = None
        self.po_box = None
        self.city = None
        self.state = None
        self.zip_code = None
        self.zip4 = None
        self.postal_code = None
        self.status = None
        self.type_id = None
        self.sequence_number = None
        self.type_code = None
        self.type_description = None


class AddressGPS(Address):
    """
    GPS coordinate for address. Follows the GPS format Heading, Degrees, Minutes, Seconds
    Attributes:
        heading_a: Direction Heading, N, S, E, W
        heading_b: Direction Heading, N, S, E, W
        degrees_a: Degree as integer
        degrees_b: Degree as integer
        minutes_a: Minutes as integer
        minutes_b: Minutes as integer
        seconds_a: Seconds as integer
        seconds_b: Seconds as integer
        address_sequence: Integer for sorting list of GPS
    """
    def __init__(self):
        super().__init__()
        self.heading_a = None
        self.heading_b = None
        self.degrees_a = None
        self.degrees_b = None
        self.minutes_a = None
        self.minutes_b = None
        self.seconds_a = None
        self.seconds_b = None
        self.address_sequence = None

