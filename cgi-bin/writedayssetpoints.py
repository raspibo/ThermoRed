#!/usr/bin/env python3

import os

import json

import cgi
import cgitb

cgitb.enable()

# Mi serve il file dei setpoins
# Se il file esiste lo apro, se no, genero entrambi SetPoints e file
with open("dayssetpointarray.json") as JsonFileDays:
	DaysSetPoints = json.load(JsonFileDays)

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


form=cgi.FieldStorage()

Error = ""	# Serve per il calcolo/verifica di errore
for j in range(len(DaysSetPoints)):
	for k in range(len(DaysSetPoints[j]["hours"])):
		StrName = str(DaysSetPoints[j]["day"])+str(k)
		#print (StrName)
		if StrName not in form:
		#if str(var) not in form:
			#print("Error")
			print("<br/>Errore:", StrName)
			Error = "Error"
		else:
			DaysSetPoints[j]["hours"][k]["temperature"] = cgi.escape(form[StrName].value)

# Se non c'e` stato nessun errore, test e` uguale alla lunghezza
# dei dati prodotti e posso sovrascrivere il file
if Error == "":
	with open('dayssetpointarray.json', 'w') as outfile:
		# Stampo a video la matrice se viene validata e inserita
		print("""
			<br/>
			<h4>Dati correttamente inseriti</h4>
			<br/>
			<p>Questo e` il risultato della matrice inserita:</p>
		""")
		print(DaysSetPoints)
		json.dump(DaysSetPoints, outfile, indent=4)

# End body/End html
print("""
</body>
</html>
""")
