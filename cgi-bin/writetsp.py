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


# Mi serve il file di configurazione, se esiste lo apro, se no setto un'errore
if os.path.exists("config.json"):
	try:
		with open("config.json") as JsonFileConfig:
			ConfigFile = json.load(JsonFileConfig)
			JsonFileConfig.close()
	except IOError:
		Error = "Errore di I/O \"config.json\""
	except ValueError:
		Error = "Errore dati \"config.json\", ritento .."
		time.sleep(5)
		with open("config.json") as JsonFileConfig:
			ConfigFile = json.load(JsonFileConfig)
			JsonFileConfig.close()
	else:
		Error = ""
else:
	Error = "Errore, non trovo il file \"config.json\""


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

print("""
<br/>
<br/>
""")


# Cerco ..
for i in range(len(ConfigFile)):
	if "temperature" == (ConfigFile[i]["name"]):
		# Appoggio a variabile l'array
		TempsArray = ConfigFile[i]["value"]


form=cgi.FieldStorage()


Error = ""	# Serve per il calcolo/verifica di errore
# Comunque, questa parte, prima di scrivere il dato, verifica che il campo non sia vuoto,
# ma ho corretto il codice html inserendo 'required', quindi ora il controllo dovrebbe
# essere inutile, ma ormai ho scritto ..
for i in range(len(TempsArray)):
	print("--")
	if TempsArray[i]["name"] not in form:
		Error = TempsArray[i]["name"]
	else:
		# Controllo se e` un numero intero
		try:
			Value = int(cgi.escape(form[TempsArray[i]["name"]].value))
		except ValueError:
			Error = TempsArray[i]["name"]+" non e` un numero intero."
		else:
			TempsArray[i]["value"] = int(cgi.escape(form[TempsArray[i]["name"]].value))


# Cerco i sensori nel file json, ma stavolta per fare il contrario, scriverli
for i in range(len(ConfigFile)):
	if "temperature" == (ConfigFile[i]["name"]):
		# Appoggio a variabile l'array
		ConfigFile[i]["value"] = TempsArray

# Se non c'e` stato nessun errore, apro e scrivo il file
if Error == "":
	with open("config.json", "w") as outfile:
		# Stampo a video la matrice se viene validata e inserita
		print("""
			<br/>
			<h4>Dati correttamente inseriti</h4>
			<br/>
			<p>Questo e` il risultato dell'inserimento:</p>
		""")
		print(TempsArray)
		#print(ConfigFile)
		json.dump(ConfigFile, outfile, indent=4)
		outfile.close()
else:
	print("<h2>Errore</h2>")
	print("<p>",Error,"</p>")


# End body/End html
print("""
</body>
</html>
""")
