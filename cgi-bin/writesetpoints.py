#!/usr/bin/env python3

import json

import cgi
import cgitb

cgitb.enable()

with open("setpointarray.json") as json_file:
    SetPoints = json.load(json_file)

# Intestazione HTML
print("<!DOCTYPE text/html>")

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

test = 0	# Serve per il calcolo/verifia di errore
for i in range(len(SetPoints)):
	if SetPoints[i]["name"] not in form:
		print("Error")
	else:
		# Sta` roba controlla se il dato inserito e` un numero intero
		try:
			Value = int(cgi.escape(form[SetPoints[i]["name"]].value))
		except ValueError:
			# Stampa a video un'errore se non e` intero
			print("""
				<br/>
				<h1>ERRORE</h1>
				<br/>
				<p>Non hai inserito un numero intero!</p>
			""")
		else:
			SetPoints[i]["temperature"] = cgi.escape(form[SetPoints[i]["name"]].value)
			test = test + 1	# Incrementa ad ogni dato valido


# Se non c'e` stato nessun errore, test e` uguale alla lunghezza
# dei dati prodotti e posso sovrascrivere il file
if test == len(SetPoints):
	with open('setpointarray.json', 'w') as outfile:
		# Stampo a video la matrice se viene validata e inserita
		print("""
			<br/>
			<h4>Dati correttamente inseriti</h4>
			<br/>
			<p>Questo e` il risultato della matrice inserita:</p>
		""")
		print(SetPoints)
		json.dump(SetPoints, outfile, indent=4)

# End body/End html
print("""
</body>
</html>
""")
