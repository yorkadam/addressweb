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
Used to build list [] of code objects for the application interfaces.
Codes represent (look-up) codes, a list of values provided as a choice
to users in an interface. Codes for this class are supplied by an external
data provider; such as a database table or file as a data source.

"""


class Code(object):
    """

        Reference and lookup codes for "type" of.. email, phone, address etc. Maps to database table "codes"

        Attributes:
            type_id:            Row identifier for the type.
            type_code:          An abbreviated type description.
            type_description:   A long description of the type.
            reference_type:     The of reference. Used to categorize reference types

    """
    def __init__(self):
        self.type_id = None
        self.type_code = None
        self.type_description = None
        self.reference_type = None
