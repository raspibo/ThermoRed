#!/usr/bin/env python

import cgi
import cgitb

cgitb.enable()

print "Content-type: text/html\n\n"

form=cgi.FieldStorage()

if "light" not in form:
    print "<h1>Neither radio button was selected.</h1>"
else:
    text=form["light"].value
    print "<h1>Radio button chosen:</h1>"
    print cgi.escape(text)

