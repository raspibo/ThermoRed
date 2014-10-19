#!/usr/bin/env python

import cgi
import cgitb

cgitb.enable()

print "Content-type: text/html\n\n"

form=cgi.FieldStorage()

if "data" not in form:
    print "<h1>The text input box was empty.</h1>"
else:
    text=form["data"].value
    print "<h1>Text from text input box:</h1>"
    print cgi.escape(text)

