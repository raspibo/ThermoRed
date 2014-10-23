#!/usr/bin/env python3

import json

import cgi
import cgitb

cgitb.enable()

with open("setpointarray.json") as json_file:
    SetPoints = json.load(json_file)

# Intestazione HTML
print("<!DOCTYPE html>")

print("""
<html>

<head>
  <title>ThermoRed</title>
  <meta name="GENERATOR" content="Midnight Commander (mcedit)">
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <meta name="Keywords" content="termoregolatore, thermo, temperatura, python">
  <meta name="Author" content="Davide">
</head>


<body>
""")	# End / Start body

print("""
<h2>Inserimento temperature di Set Point</h2>
<p><b>ATTENZIONE</b>: Accetta solo valori (numeri) interi.</p?
<br/>
<br/>
""")

# Start form input
print("<form action=\"/cgi-bin/writesetpoints.py\" method=\"post\">")

for i in range(len(SetPoints)):
	#print(SetPoints[i]["display"])
	#print(":")
	#print("<input type=\"text\" name=\"")
	#print(SetPoints[i]["name"])
	#print("\" value=\"")
	#print(SetPoints[i]["temperature"])
	#print("\" required><br/>")A
	print(SetPoints[i]["display"],":<input type=\"text\" size=\"5\" name=\"",SetPoints[i]["name"],"\" value=\"",SetPoints[i]["temperature"],"\" required><br/>", sep="")

print("<input type=\"submit\" value=\"Submit\">")
print("</form>")	# END form


# End body/End html
print("""
</body>
</html>
""")
