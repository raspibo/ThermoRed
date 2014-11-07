#!/usr/bin/env python3

# Scrive il file di configurazione,
# con i dati ricevuti dal rispettivo "read*.py"

# Serve per controllare i files
import os

# Serve per il formato dati, il file di configurazione e`
# in struttura "json"
import json

# Serve per la parte di gestione html in python
import cgi
import cgitb

import time
# Abilita gli errori al server web/http
cgitb.enable()


# Mi servono i files di configurazione, se esistono li apro, se no setto un'errore
if os.path.exists("weektsp.json"):
	try:
		with open("weektsp.json") as JsonFileWtsp:
			WtspFile = json.load(JsonFileWtsp)
			JsonFileWtsp.close()
	except IOError:
		Error = "Errore di I/O \"weektsp.json\""
	except ValueError:
		Error = "Errore dati \"weektsp.json\", ritento .."
		time.sleep(5)
		with open("weektsp.json") as JsonFileWtsp:
			WtspFile = json.load(JsonFileWtsp)
			JsonFileWtsp.close()
	else:
		Error = ""
else:
	Error = "Errore, non trovo il file \"weektsp.json\""


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

## Inizio pagina web

# Stampa errore se c'e` stato
if Error != "":
	print("<h1>",Error,"</h1><br/>")

form=cgi.FieldStorage()

for j in range(len(WtspFile)):
	for k in range(len(WtspFile[j]["hours"])):
		StrName = str(WtspFile[j]["day"])+str(k)
		#print (StrName)
		if StrName not in form:
		#if str(var) not in form:
			#print("Error")
			print("<br/>Errore:", StrName)
			Error = "Error"
		else:
			WtspFile[j]["hours"][k]["temperature"] = cgi.escape(form[StrName].value)


# Se non c'e` stato nessun errore, apro e scrivo il file
if Error == "":
	with open("weektsp.json", "w") as outfile:
		# Stampo a video la matrice se viene validata e inserita
		print("""
			<br/>
			<h4>Dati correttamente inseriti</h4>
			<br/>
			<p>Questo e` il risultato dell'inserimento:</p>
		""")
		print(WtspFile)
		json.dump(WtspFile, outfile, indent=4)
		outfile.close()
else:
	print("<h2>Errore</h2>")
	print("<p>",Error,"</p>")



# End body/End html
print("""
</body>
</html>
""")
