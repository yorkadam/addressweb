import os
import cherrypy
import datetime
from addressbook.data.identifiers import random_char
from addressbook.data.read import is_person_identifier_used

from addressbook.data.create import create_person, create_address, create_phone_contact, create_email_contact,\
    create_identification, create_relation, create_comment

from addressbook.data.read import search_people_2, search_people_1, read_people

from addressbook.data.update import update_person, update_address, update_phone_contact, update_email_contact, \
    update_identification, update_comment

from addressbook.data.delete import delete_person, delete_address, delete_contact, delete_identification, \
    delete_relationship

from addressbook.data.read import read_addresses, read_phone_contacts, read_email_contacts, read_relationships, \
    read_identification, read_comment, read_relationship_map

from addressbook.models.people import Person, Comment, Relationship2
from addressbook.models.addresses import Address
from addressbook.models.contacts import Phone, Email
from addressbook.models.identities import Identity
from jinja2 import Environment, FileSystemLoader

# TODO: In general add expected error handling to exception blocks and / or refactor into logging module instead.
# TODO: move environment settings and cherry startup configs / calls to separate module.
env = Environment(loader=FileSystemLoader('views'))

# TODO: replace hard coded list with database lookup and refactor to correct location. Also, move header to correct spot
relationship_list = [("SIBLING", 1), ("PARTNER", 2),("CHILD-STEP", 3), ("NIBLING", 4), ("CHILD", 5), ("PARAMORE", 6),
                     ("PARENT-SIBLING", 7), ("GRAND-CHILD", 8), ("GRAND-PARENT", 9), ("FRIEND", 10), ("COUSIN", 11),
                     ("PARENT-STEP", 12), ("PARENT-INLAW", 13), ("PARENT", 14), ("CHILD-INLAW", 15), ("SPOUSE", 16)]

relationship_search_header = ["PID", "First Name", "Last Name", "Middle Ini.", "Nickname", "Date of Birth",
                              "Date of Death", "Relation Type"]

relationship_search_rows = []


class Root:
    @cherrypy.expose
    def index(self, **kwargs):
        address_rows = []
        phone_rows = []
        email_rows = []
        relation_rows = []
        id_rows = []
        comments = []
        comment_text = ""
        comment_id = ""
        selected_name = ""

        try:
            if kwargs is not None and len(kwargs) > 0:
                if kwargs.get("search_button"):
                    people = self.search(**kwargs)
                elif kwargs.get("save_button_person"):
                    person = Person()
                    person.person_id = random_char(26)
                    person.first_name = kwargs["first_name"]
                    person.last_name = kwargs["last_name"]
                    person.middle_initial = kwargs["middle_initial"]
                    person.nick_name = kwargs["nick_name"]
                    person.date_of_birth = kwargs["birth_date"]
                    person.date_of_death = kwargs["death_date"]
                    self.add_person2(person)
                    people = read_people()
                elif kwargs.get("update_button_person"):
                    person = Person()
                    person.person_id = kwargs["person_id"]
                    person.first_name = kwargs["first_name"]
                    person.last_name = kwargs["last_name"]
                    person.middle_initial = kwargs["middle_initial"]
                    person.nick_name = kwargs["nick_name"]
                    person.date_of_birth = kwargs["birth_date"]
                    person.date_of_death = kwargs["death_date"]
                    update_person(person)
                    people = read_people()
                elif kwargs.get("delete_button_person"):
                    delete_person(kwargs["person_id"])
                    people = read_people()
                elif kwargs.get("selected_person_id"):
                    addresses = read_addresses(kwargs["selected_person_id"])
                    phone_contacts = read_phone_contacts(kwargs["selected_person_id"])
                    email_contacts = read_email_contacts(kwargs["selected_person_id"])
                    relationships = read_relationships(kwargs["selected_person_id"])
                    identification_cards = read_identification(kwargs["selected_person_id"])
                    comments = read_comment(kwargs["selected_person_id"])
                    cherrypy.session["selected_person_id"] = kwargs["selected_person_id"]
                    people = read_people()

                    for person in people:  # will only be 1 person here due to specific id
                        if person.person_id == kwargs["selected_person_id"]:
                            selected_name = person.first_name + " " + person.last_name

                    for address in addresses:
                        address_link_edit = "<a id='ae_{0}' href=http://localhost:edit?pid='{1}' " \
                                            "onclick=addressHandler(this,'{2}'); data-address-action=edit>" \
                                            "edit</a>".format(address.person_id, address.person_id, address.person_id)

                        address_link_delete = "<a id='ad_{0}' href=http://localhost:delete?pid='{1}' " \
                                              "onclick=addressHandler(this,'{2}'); " \
                                              "data-address-action=delete>delete</a>".format(address.person_id,
                                                                                             address.person_id,
                                                                                             address.person_id)

                        address_rows.append((address_link_edit, address.address_id, address.person_id,
                                             address.address_line_1, address.address_line_2, address.po_box,
                                             address.city, address.state, address.zip_code, address.zip4,
                                             address.postal_code, address.status, address.sequence_number,
                                             address.type_id, address.type_description, address_link_delete))

                    for phone in phone_contacts:

                        phone_link_edit = "<a id='pe_{0}' href=http://localhost:edit?pid='{1}' " \
                                          "onclick=phoneHandler(this,'{2}'); data-phone-action=edit>" \
                                          "edit</a>".format(phone.person_id, phone.person_id, phone.person_id)

                        phone_link_delete = "<a id='pd_{0}' href=http://localhost:delete?pid='{1}' " \
                                            "onclick=phoneHandler(this,'{2}'); data-phone-action=delete>" \
                                            "delete</a>".format(phone.person_id, phone.person_id, phone.person_id)

                        phone_rows.append((phone_link_edit, phone.contact_id, phone.phone_type_id,
                                           phone.sequence_number, phone.area_code, phone.exchange, phone.trunk,
                                           phone.area_code + "-" + phone.exchange + "-" + phone.trunk,
                                           phone.type_description, phone_link_delete))

                    for email in email_contacts:

                        email_link_edit = "<a id='ee_{0}' href=http://localhost:edit?pid='{1}' " \
                                          "onclick=emailHandler(this,'{2}'); data-email-action=edit>" \
                                          "edit</a>".format(email.person_id, email.person_id, email.person_id)

                        email_link_delete = "<a id='ed_{0}' href=http://localhost:delete?pid='{1}' " \
                                            "onclick=emailHandler(this,'{2}'); data-email-action=delete>" \
                                            "delete</a>".format(email.person_id, email.person_id, email.person_id)

                        email_rows.append((email_link_edit, email.contact_id, email.email_address,
                                           email.sequence_number, email.type_code, email.type_description,
                                           email_link_delete))

                    for relationship in relationships:
                        id_link_delete = "<a id='rid_{0}' href=http://localhost:delete?rid='{1}' " \
                                         "onclick=relationshipHandler(this,'{2}'); data-relationship-action=" \
                                         "delete>delete</a>".format(relationship.relationship_id,
                                                                    relationship.relationship_id,
                                                                    relationship.relationship_id)

                        relation_rows.append((relationship.person.first_name, relationship.person.last_name,
                                              relationship.person.middle_initial,
                                              relationship.relationship_type_description, id_link_delete))

                    for identity in identification_cards:

                        id_link_edit = "<a id='ie_{0}' href=http://localhost:edit?pid='{1}' " \
                                       "onclick=identificationHandler(this,'{2}'); data-identification-action=edit>" \
                                       "edit</a>".format(identity.person_id, identity.person_id, identity.person_id)

                        id_link_delete = "<a id='id_{0}' href=http://localhost:delete?pid='{1}' " \
                                         "onclick=identificationHandler(this,'{2}'); " \
                                         "data-identification-action=delete>delete</a>".format(identity.person_id,
                                                                                               identity.person_id,
                                                                                               identity.person_id)

                        id_rows.append((id_link_edit, identity.person_id, identity.identification_number,
                                        identity.type_code_id, identity.type_description, identity.issuing_authority,
                                        identity.issuing_entity, identity.record_location, identity.identification_id,
                                        id_link_delete))

                    for comment in comments:
                        comment_text = comment.comment
                        comment_id = comment.comment_id
            elif kwargs is not None and len(kwargs) == 0:
                people = read_people()

            address_header = ["Edit", "addressid", "personid", "Address Line 1", "Line 2", "pobox", "City", "State",
                              "Zip Code", "zip4", "postalcode", "status", "Sequence", "typeid", "Type Description",
                              "Delete"]

            search_header = ["Select","Edit", "PersonId","First Name", "Last Name", "Middle Ini.",
                             "Nick Name", "Date of Birth", "Date of Death", "Delete"]

            phone_header = ["Edit", "CID", "Type Id", "Sequence", "Area", "Exchange", "Trunk", "Phone Number",
                            "Type Desc.", "Delete"]

            email_header = ["Edit", "CID", "Email Address", "Sequence", "Type Id", "Type Desc.", "Delete"]

            relation_header = ["First Name", "Last Name", "Middle Ini.", "Relationship Type", "Delete"]

            id_header = ["Edit", "PersonId", "ID Number", "ID Type", "ID Type Description", "Issuing Authority",
                         "Issuing Entity", "Record Location", "IdentificationId", "Delete"]

            search_rows = []
            for person in people:
                # <a href="https://docs.python.org/2/library/functions.html#vars">sdfdfsd</a>

                link_edit = "<a id='{0}' href=http://localhost:edit?pid='{1}' onclick=openPersonDialog(this,'{2}'); " \
                            "data-person-action=edit>edit</a>".format(person.person_id,
                                                                      person.person_id,
                                                                      person.person_id)

                link_delete = "<a id='_{0}' href=http://localhost:delete?pid='{1}' " \
                              "onclick=openPersonDialog(this,'{2}'); data-person-action=delete>" \
                              "delete</a>".format(person.person_id, person.person_id, person.person_id)

                column_select = "<a id='__{0}' href=http://localhost:edit?pid='{1}' onclick=selectRow(this,'{2}'); " \
                                "data-person-action=select>View</a>".format(person.person_id,
                                                                            person.person_id,
                                                                            person.person_id)
                search_rows.append((column_select, link_edit, person.person_id, person.first_name, person.last_name,
                                    person.middle_initial, person.nick_name, person.date_of_birth, person.date_of_death,
                                    link_delete))

            template = env.get_template('dashboard/index.html')

            return template.render(relation_header=relation_header, relation_rows=relation_rows, id_header=id_header,
                                   id_rows=id_rows, address_header=address_header, address_rows=address_rows,
                                   email_header=email_header, email_rows=email_rows, phone_header=phone_header,
                                   phone_rows=phone_rows, search_header=search_header, search_rows=search_rows,
                                   widget_identifer="", comment_text=comment_text, comment_id=comment_id,
                                   selected_person=cherrypy.session.get('selected_person_id'),
                                   selected_name=selected_name, relationship_search_header=relationship_search_header,
                                   relationship_search_rows=relationship_search_rows,
                                   relationship_list=relationship_list)
        except Exception as exception:
            pass

    def add_person2(self, person):
        # First and last names are required to save. So before save check if provided.
        if len(person.first_name) == 0 or len(person.last_name) == 0:
            # TODO: setup ajax response here with ajax we cannot just return
            # so this validation as well as the others below will need to be tweaked.
            # return
            pass
        # Dates (DOB and DOD) not required but if present must be valid dates.
        # Expected date format is: YYYY-MM-DD
        if len(person.date_of_birth) > 0 or len(person.date_of_death) > 0:
            try:
                date_value = None
                if len(person.date_of_birth) > 0:
                    date_value = person.date_of_birth.split("-")
                if len(person.date_of_death) > 0:
                    date_value = person.date_of_death.split("-")

                datetime.datetime(int(date_value[0]), int(date_value[1]), int(date_value[2]))
                #TOTO: Add exception handling for value, type, and index errors
            except:
                pass
        # Before we create a person record we need to make sure that the
        # identifier for the person record has not already been used.
        # If used = yes then get new identifier
        # if used = no then okay to use identifier

        # set an iteration limit here to prevent endless looping as it should be extremely
        # rare, we still want to check if there is a problem if we cannot find an unused
        # random identifier. For example, if we cannot find a random identifier in 5000 tries
        # we need to re-evaluate the use of random for identifiers.
        iteration_limit = 5000
        iterator_value = 0
        while is_person_identifier_used(person.person_id):
            person.person_id = random_char(26)
            iterator_value += 1
            if iterator_value == iteration_limit:
                break
        # if we hit 5000+ then just quit don't try to add a record (UI needs to be notified)
        if iterator_value >= 5000:
            # TODO: Error handling for exceeding limit
            pass
        else:
            result = create_person(person)
            if result.value:
                comment = Comment()
                comment.person_id = person.person_id
                comment.comment = ""
                comment.comment_id = None
                create_comment(comment)
                pass
                # TODO: add success feedback if needed.
            else:
                # TODO: handle error here as well
                pass
        return "Completed At End"

    def add_relationship(self, relationship):
        relationship_map = read_relationship_map()
        selected_relationship_type_value = ""  # The string value of the choice.
        mapped_relationship_value = ""
        result = None

        for key in relationship_map:
            if key == relationship.relationship_type:
                selected_relationship_type = relationship_map[key]
                selected_relationship_type_value = selected_relationship_type[2]
                mapped_relationship_value = relationship_map[selected_relationship_type[1]][2]
                relationship.relationship_type = mapped_relationship_value
                relationship.related_person_relationship_type = selected_relationship_type_value
                relationship.relationship_type_description = selected_relationship_type[0]
                result = create_relation(relationship)
                return result
                # when result is None we cannot get positional argument
                # TODO: decide how to handle when a match against types is not found
                # Rule: to correctly insert relationship there MUST be a match on type found otherwise error

        pass
    # TODO: decide if we want to keep the following def calls as they might be redundant if we can call the
    # database methods directly... However, maybe we want it separate from DB stuff
    # so that we ca swap out databases if needed without having to change this file.

    def add_address(self, address):
        # todo add input validation here
        result = create_address(address)
        return result

    def update_address(self, address):
        # todo add input validation here.
        update_address(address)

    def add_phone(self, phone):
        # todo add input validation here.
        result = create_phone_contact(phone)
        return result

    def update_phone(self, phone):
        # todo add input validation here
        update_phone_contact(phone)

    def add_email(self, email):
        # todo add input validation here
        result = create_email_contact(email)
        return result

    def update_email(self, email):
        # todo add input validation here
        update_email_contact(email)

    def add_identification(self, identity):
        # todo add input validation here
        result = create_identification(identity)
        return result

    def update_identification(self, identity):
        # todo add input validation here
        update_identification(identity)

    def search(self, **search_form):
        # Form fields
        # search_criteria is the input field that supplies the actual filer value
        # search_predicate is for contains or equals
        # search_button is the search submit button
        # search_options is for the drop down list of filters

        search_type_option = None
        search_value = None
        search_predicate = None

        if "search_predicate" in search_form:
            search_predicate = search_form["search_predicate"]
            pass

        if "search_options" in search_form:
            search_type_option = search_form["search_options"]
            pass

        if "search_criteria" in search_form:
            search_value = search_form["search_criteria"]

        if search_value == "":
            search_value = None

        people = []
        # Search rule: If radio not selected assume "Contains" value as search.
        # search 1: Equals (case insensitive) sql "="
        # search 2: Contains (case insensitive) sql "LIKE %?%"
        if search_predicate is None:
            people = search_people_2(search_type_option, search_value)
            return people
            # self.search_inputs.variable_radio_option.set(2)
        if search_predicate == "contains":
            people = search_people_2(search_type_option, search_value)
            return people
        if search_predicate == "equals":
            people = search_people_1(search_type_option, search_value)
            return people
            # self.index(search=people)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.tools.allow(methods=['POST'])
    def relation_search(self):
        search_predicate = None
        search_value = None
        input_json = cherrypy.request.json
        search_type_option = None
        for item in input_json:
            name = item["name"]
            value = item["value"]
            if name == "relation_search_options":
                search_type_option = value
            elif name == "relation_search_predicate":
                search_predicate = value
            elif name == "relation_search_criteria":
                search_value = value

        if search_value == "":
            search_value = None

        if search_predicate is None:
            people = search_people_2(search_type_option, search_value)

        if search_predicate == "contains":
            people = search_people_2(search_type_option, search_value)

        if search_predicate == "equals":
            people = search_people_2(search_type_option, search_value)

        people_list = []

        for person in people:
            people_list.append(vars(person))

        return people_list

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.tools.allow(methods=['POST'])
    def relation_create(self):
        input_json = cherrypy.request.json
        output_json = []

        for item in input_json:
            pid = item["selectedPid"]
            sid = item["relatedPid"]
            stype = item["relatedType"]
            relationship = Relationship2()
            relationship.person_id = pid
            relationship.related_person_id = sid
            relationship.relationship_type = stype
            relationship.first_name = item["first_name"]
            relationship.last_name = item["last_name"]
            relationship.middle_initial = item["middle_ini"]
            result = self.add_relationship(relationship)
            relationship.relationship_id = result[1]
            output_json.append(vars(relationship))

            # TODO: error handling needs to be added here to catch array / subscript errors [0], [1] etc
            # because None type has no positions and we could possibly get a None
            # type on two things: 1. trying to match relation types or 2. trying to do insert.
            # so, in general error handling every where but this is a first priority
            # because in some cases a record can get added and unless all records are added correctly
            # we should not add any. Meaning, if all don't insert then roll-back any that
            # have already been processed or inserted.
        return output_json

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.tools.allow(methods=['POST'])
    def relation_delete(self):
        input_json = cherrypy.request.json
        relationship_id = input_json["id"]
        delete_relationship(relationship_id)
        # TODO: error handling here

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.tools.allow(methods=['POST'])
    def phone_update(self):
        input_json = cherrypy.request.json
        phone = Phone()
        phone.contact_id = input_json["phone_cid"]
        phone.sequence_number = input_json["phone_sequence_number"]
        phone.area_code = input_json["phone_area_code"]
        phone.exchange = input_json["phone_exchange"]
        phone.trunk = input_json["phone_trunk"]
        phone.person_id = input_json["phone_pid"]
        phone.type_code = input_json["phone_type"]
        phone.type_description = input_json["phone_type_description"]
        self.update_phone(phone)
        return vars(phone)  # TODO: error handling here

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.tools.allow(methods=['POST'])
    def phone_create(self):
        input_json = cherrypy.request.json
        phone = Phone()
        phone.sequence_number = input_json["phone_sequence_number"]
        phone.area_code = input_json["phone_area_code"]
        phone.exchange = input_json["phone_exchange"]
        phone.trunk = input_json["phone_trunk"]
        phone.person_id = input_json["phone_pid"]
        phone.type_code = input_json["phone_type"]
        phone.type_description = input_json["phone_type_description"]
        result = self.add_phone(phone)
        phone.contact_id = result.value  # result[1]  # input_json["phone_cid"]
        phone.message = result.message  # adding message attribute is one way to use Python's dynamic nature.
        phone.error_status = result.error_status
        phone.success = result.success
        return vars(phone)  # TODO: error handling here

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.tools.allow(methods=['POST'])
    def phone_delete(self):
        input_json = cherrypy.request.json
        phone = Phone()
        phone.contact_id = input_json["phone_cid"]
        phone.sequence_number = input_json["phone_sequence_number"]
        phone.area_code = input_json["phone_area_code"]
        phone.exchange = input_json["phone_exchange"]
        phone.trunk = input_json["phone_trunk"]
        phone.person_id = input_json["phone_pid"]
        phone.type_code = input_json["phone_type"]
        phone.type_description = input_json["phone_type_description"]
        delete_contact(phone.contact_id)
        return vars(phone)  # TODO: error handling here

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.tools.allow(methods=['POST'])
    def email_update(self):
        input_json = cherrypy.request.json
        email = Email()
        email.contact_id = input_json["email_cid"]
        email.sequence_number = input_json["email_sequence_number"]
        email.person_id = input_json["email_pid"]
        email.type_code = input_json["email_type_id"]
        email.type_description = input_json["email_type_description"]
        email.email_address = input_json["email_address"]
        self.update_email(email)
        return vars(email)  # TODO: error handling here

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.tools.allow(methods=['POST'])
    def email_create(self):
        input_json = cherrypy.request.json
        email = Email()
        email.contact_id = input_json["email_cid"]
        email.sequence_number = input_json["email_sequence_number"]
        email.person_id = input_json["email_pid"]
        email.type_code = input_json["email_type_id"]
        email.type_description = input_json["email_type_description"]
        email.email_address = input_json["email_address"]
        result = self.add_email(email)
        email.contact_id = result[1]
        return vars(email)  # TODO: error handling here

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.tools.allow(methods=['POST'])
    def email_delete(self):
        input_json = cherrypy.request.json
        email = Email()
        email.contact_id = input_json["email_cid"]
        email.sequence_number = input_json["email_sequence_number"]
        email.person_id = input_json["email_pid"]
        email.type_code = input_json["email_type_id"]
        email.type_description = input_json["email_type_description"]
        email.email_address = input_json["email_address"]
        delete_contact(email.contact_id)
        return vars(email)  # TODO: error handling here

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.tools.allow(methods=['POST'])
    def address_update(self):
        input_json = cherrypy.request.json
        address = Address()
        address.address_id = input_json["address_aid"]
        address.sequence_number = input_json["address_sequence_number"]
        address.person_id = input_json["address_pid"]
        address.type_code = input_json["address_type"]
        address.type_id = input_json["address_type"]
        address.type_description = input_json["address_type_description"]
        address.address_line_1 = input_json["address_line_1"]
        address.address_line_2 = input_json["address_line_2"]
        address.po_box = input_json["po_box"]
        address.city = input_json["city"]
        address.state = input_json["state"]
        address.zip_code = input_json["zip_code"]
        address.zip4 = input_json["zip_4"]
        address.postal_code = input_json["postal_code"]
        address.status = input_json["address_status"]
        # address_type: address_type_value,
        # address_type_description: address_type_description
        self.update_address(address)
        return vars(address)  # TODO: error handling here

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.tools.allow(methods=['POST'])
    def address_create(self):
        input_json = cherrypy.request.json
        address = Address()
        address.sequence_number = input_json["address_sequence_number"]
        address.person_id = input_json["address_pid"]
        address.type_code = input_json["address_type"]
        address.type_id = input_json["address_type"]
        address.type_description = input_json["address_type_description"]
        address.address_line_1 = input_json["address_line_1"]
        address.address_line_2 = input_json["address_line_2"]
        address.po_box = input_json["po_box"]
        address.city = input_json["city"]
        address.state = input_json["state"]
        address.zip_code = input_json["zip_code"]
        address.zip4 = input_json["zip_4"]
        address.postal_code = input_json["postal_code"]
        address.status = input_json["address_status"]
        result = self.add_address(address)
        address.address_id = result[1]
        return vars(address)  # TODO: error handling here

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.tools.allow(methods=['POST'])
    def address_delete(self):
        input_json = cherrypy.request.json
        address = Address()
        address.address_id = input_json["address_aid"]
        address.sequence_number = input_json["address_sequence_number"]
        address.person_id = input_json["address_pid"]
        address.type_code = input_json["address_type"]
        address.type_id = input_json["address_type"]
        address.type_description = input_json["address_type_description"]
        address.address_line_1 = input_json["address_line_1"]
        address.address_line_2 = input_json["address_line_2"]
        address.po_box = input_json["po_box"]
        address.city = input_json["city"]
        address.state = input_json["state"]
        address.zip_code = input_json["zip_code"]
        address.zip4 = input_json["zip_4"]
        address.postal_code = input_json["postal_code"]
        address.status = input_json["address_status"]
        delete_address(address.address_id)
        return vars(address)  # TODO: error handling here

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.tools.allow(methods=['POST'])
    def identification_update(self):
        input_json = cherrypy.request.json
        identification = Identity()
        identification.person_id = input_json["identification_pid"]
        identification.identification_id = input_json["identification_id"]
        identification.identification_number = input_json["identification_number"]
        identification.issuing_authority = input_json["issuing_authority"]
        identification.issuing_entity = input_json["issuing_entity"]
        identification.record_location = input_json["record_location"]
        identification.type_code = input_json["identification_type"]
        identification.type_description = input_json["identification_type_description"]
        self.update_identification(identification)
        return vars(identification)  # TODO: error handling here

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.tools.allow(methods=['POST'])
    def identification_create(self):
        input_json = cherrypy.request.json
        identification = Identity()
        identification.person_id = input_json["identification_pid"]
        identification.identification_number = input_json["identification_number"]
        identification.issuing_authority = input_json["issuing_authority"]
        identification.issuing_entity = input_json["issuing_entity"]
        identification.record_location = input_json["record_location"]
        identification.type_code = input_json["identification_type"]
        identification.type_description = input_json["identification_type_description"]
        result = self.add_identification(identification)
        identification.identification_id = result[1]
        return vars(identification)  # TODO: error handling here

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.tools.allow(methods=['POST'])
    def identification_delete(self):
        input_json = cherrypy.request.json
        identification = Identity()
        identification.person_id = input_json["identification_pid"]
        identification.identification_id = input_json["identification_id"]
        identification.identification_number = input_json["identification_number"]
        identification.issuing_authority = input_json["issuing_authority"]
        identification.issuing_entity = input_json["issuing_entity"]
        identification.record_location = input_json["record_location"]
        identification.type_code = input_json["identification_type"]
        identification.type_description = input_json["identification_type_description"]
        delete_identification(identification.identification_id)
        return vars(identification)  # TODO: error handling here

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.tools.allow(methods=['POST'])
    def comment_update(self):
        input_json = cherrypy.request.json
        comment = Comment()
        comment.person_id = input_json["comment_pid"]
        comment.comment_id = input_json["comment_id"]
        comment.comment = input_json["comment"]
        update_comment(comment)
        return vars(comment)  # TODO: error handling here


# cherrypy.config.defaults["tools.staticdir.on"] = True
# cherrypy.config.defaults["tools.staticdir.dir"] = "/views/assets"

# static_path = "/home/adam/PycharmProjects/addressweb/addressbook/views/assets"
location = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'views')

conf = {
     '/': {
         'tools.staticdir.on': True,
         'tools.staticdir.dir': 'assets',
         'tools.staticdir.root': location,
         'tools.sessions.on': True,
     }
}

cherrypy.quickstart(Root(), '/', conf)

# cherrypy.quickstart(Root())
