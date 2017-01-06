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


""" Class as object.
Class in this module represents an Identity, such as, a drivers license, a social security card,
or other type of identification.
"""


class Identity(object):
    """

        A identification class for identification cards, such as drivers license.

        Attributes:
        person_id:              The person identifier for which the identity belongs.
        identification_number:  The identification number documented on the identification card.
        issuing_authority:      The governing authority which authorizes entities to issue identification.
        issuing_entity:         The issuing entity as indicated by the issuing authority. May be the same but often not.
        record_location:        A location of the record. May be a file path or simply a comment about where to find.
        identification_id:      The row identifier for the identity.
        type_code:              The identification type such as drivers license, social security card, and sheriff
        id card etc.
    """
    def __init__(self):
        self.person_id = None
        self.identification_number = None
        self.issuing_authority = None
        self.issuing_entity = None
        self.record_location = None
        self.identification_id = None
        self.type_code = None
