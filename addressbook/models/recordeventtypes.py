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
Enumerations for data model actions.
"""


from enum import Enum


class DeleteRecord(Enum):
    """ Enum: Delete actions. """
    person = 1
    address = 2
    relation = 3
    phone = 4
    email = 5
    identification = 6


class SaveRecord(Enum):
    """ Enum: Save actions. """
    person = 1
    address = 2
    relation = 3
    phone = 4
    email = 5
    identification = 6


class EditRecord(Enum):
    """ Enum: Edit actions."""
    person = 1
    address = 2
    relation = 3
    phone = 4
    email = 5
    identification = 6


class CreateRecord(Enum):
    """Enum: Create actions."""
    person = 1
    address = 2
    relation = 3
    phone = 4
    email = 5
    identification = 6
