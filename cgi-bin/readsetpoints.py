#!/usr/bin/env python3

import os

import json

import cgi
import cgitb

cgitb.enable()

# Se il file esiste lo apro, se no, genero entrambi SetPoints e file
if os.path.exists("setpointarray.json"):
	with open("setpointarray.json") as json_file:
		SetPoints = json.load(json_file)
else:
	SetPoints = \
		[	\
		    { "display": "Temperatura Giorno", "name": "Tday", "temperature": "20" },	\
		    { "display": "Temperatura Notte", "name": "Tnight", "temperature": "16" },	\
		    { "display": "Temperatura Antigelo", "name": "Tice", "temperature": "5" },	\
		]
	
	with open("setpointarray.json", "w") as outfile:
		json.dump(SetPoints, outfile, indent=4)


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
<p><b>ATTENZIONE</b>: Accetta solo valori (numeri) interi.</p>
<p>Numeri da 5 (min) a 30 (max).</p>
<br/>
<br/>
""")

# Start form input
print("<form action=\"/cgi-bin/writesetpoints.py\" method=\"post\">")
print("<table>")

# Per tutta la lunghezza/voci contenute nell'array ..
for i in range(len(SetPoints)):
	# Concatenamento di variabili da SetPoins e pezzi di html
	print("<tr><td>",SetPoints[i]["display"],":</td><td><input type=\"number\" name=\"",SetPoints[i]["name"],"\" value=\"",SetPoints[i]["temperature"],"\" min=\"5\" max=\"30\" maxlength=\"2\" size=\"2\" required><br/></td></tr>", sep="")

print("<td></td><td><input type=\"submit\" value=\"Submit\"></td>")
print("</table>")
print("</form>")	# END form


# End body/End html
print("""
</body>
</html>
""")
