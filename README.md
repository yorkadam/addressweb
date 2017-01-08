# addressweb - HTML & Python Based Address Book
Please note: I am currently a Software Engineer; where at work we use the Microsoft stack for everything. This project is one of many non-Microsoft projects I'm working on to solidify my skills on other technology stacks.  Therefore, this is a learning project for me and I would be happy to receive any feedback positive or negative. 
## Description
A simple stand-alone address book for keeping track of people’s addresses, contact information, identification, and relationships. 
This address book software is written in Python, javascript, html, SQLite, JQuery UI,  and uses CherryPy.

## Why create another address book?

I created this address book because I was frustrated with current address book solutions which try to integrate everything. 
The current software-industry ( or projects ) trend towards pushing users personal information into the cloud is alarming, 
not so-much about where the data is stored but how badly data is leaked, hacked, and compelled ( by law enforcement ) 
for data access. Additionally, cloud services have let me down by corrupting my data, failing to secure my data, 
and the worse offense of all; deleting my data when I needed it most.

Perhaps, more simply-put, I wanted an address book that no-one may control but me, is simple, and cloudless. 
After all clouds mean rain and I’ve had enough of it.

### Devices & Display Intent
This software was written as a stand alone (self hosted) web-based application for display on PC/Desktop devices. No testing has been done for anything other than IE,FF and Chrome on a desktop browser. I don't know if it will work on mobile devices or not. However, reasonably sized tablets might be usable. Devices that can support JQuery UI (not mobile ui) should be fine.

## Features
This is a standard contacts based address book that includes, phone, email, addresses, comments and basic search features.  Additionally, I added features that I personally find useful to me that include the following:

Identification: Used to track ID cards and card issuers. This feature is useful if are responsible for keeping track of ID cards for your contacts, or perhaps if you are a traveler and hate to yank your physical passport, visa's and other ID from the file cabinet just to enter data into a web form.

Relationships: Used to relate individual entries by familiar connections. This feature is useful to me because I found keeping track of a sprawling family and related children, grandchildren, nieces and nephews... you get the point; whom is related to whom is good to know when sending birthday and Christmas presents because it's awkward to mistakenly send gifts to only one of three children. (-: The relationship feature maps relationships both directions. Meaning, if you mark a person as your child you are automatically marked as parent on the corresponding record.

## Documentation
Documentation is in the works for this version. However, the general functionality is similar to the non-web-based version I created in python and Tkinter. Below is the Tkinter version, documentation, and location:

Documentation: 
http://adamyork.com/projects/address-book/ 

Tkinter Version:
https://pypi.python.org/pypi/addressbook/1.0.1

### Setup & Cofiguration
This project was written using the PyCharm 5.0.4 toolkit. I have included the complete PyCharm project files for anyone who wants to use PyCharm.

As for setup, this is a CherryPy project, simply copy the source code to a directory and start the project using the main.py file from the command line. This will start CherryPy on the local host and you can run the application from your favorite browser. Please remember to change the CheryPy settings to values appropriate for your system and environment.

### Requirements
This project is using Python 3.4, SQlite, and CherryPy your local python envrionment will need these installed to work correctly. My suggestion is to use virtualenv to install and run the project.

### Theming
I used the JQuery theme roller to build a customized theme. People who wish to change the theme just need to replace the existing theme roller files with a new roller theme and tweak any additional CSS in the main files that doesn't match the theme.

## Attribution

CREATED BY: Adam York

CONTACT: code@adamyork.com

LICENSE: MIT

OPERATING SYSTEMS: Cross platform

PROGRAMMING LANGUAGE: Python 3.4

WEBSITE: http://www.adamyork.com/projects/

>Please be kind and properly attribute my work however it is used in either source code form or application form.  
>Please use the information is the Attribution section above.
