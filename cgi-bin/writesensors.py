#!/usr/bin/env python3

# Questo file legge il file di configurazione,
# trova e modifica il parametro eseguando il "writeconfig.py"

# Serve per controllare i files
import os

# Serve per il formato dati, il file di configurazione e`
# in struttura "json"
import json

# Serve per la parte di gestione html in python
import cgi
import cgitb

# Abilita gli errori al server web/http
cgitb.enable()


# Mi serve il file di configurazione, se esiste lo apro, se no setto un'errore
if os.path.exists("config.json"):
	with open("config.json") as JsonFileConfig:
		ConfigFile = json.load(JsonFileConfig)
	Error = ""
else:
	Error = "Si e\` verificato un\'errore, non trovo il file \"config.json\""

# Directory dei device 1 wire
for i in range(len(ConfigFile)):
	if "dir1w" == (ConfigFile[i]["name"]):
		# Appoggio a variabile
		Dir1wire = ConfigFile[i]["value"]


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
<h2>Configurazione sensori temperatura</h2>
<p><b>ATTENZIONE</b>: Devo ancora scrivere l'help/guida</p>
<p>???</p>
<br/>
<br/>
""")

# Stampo sulla pagina web il listato della directory dei sensori 1wire
# teoricamente e` da togliere sempre l'ultimo risultato,
# suggerisco di lasciarlo visibile, tanto non dovrebbe infastidire.
print("<h3>Lista dei sensori configurati</h3>")
print("<p></p><br/>")

print("<p><hr/></p><br/>")	# Stampa un linea orizzontale

# Cerco i sensori nel file json
for i in range(len(ConfigFile)):
	if "sensori" == (ConfigFile[i]["name"]):
		# Appoggio a variabile l'array
		SensoriArray = ConfigFile[i]["value"]

form=cgi.FieldStorage()

Error = ""	# Serve per il calcolo/verifica di errore
# Come cazzo la spiego ?
for j in range(len(SensoriArray)):
	DisplayN = "display"+str(j)
	if DisplayN not in form:
		print("<br/>Errore:", DisplayN)
		Error = DisplayN
	else:
		SensoriArray[j]["display"] = cgi.escape(form[DisplayN].value)
	NameN = "name"+str(j)
	if NameN not in form:
		print("<br/>Errore:", NameN)
		Error = NameN
	else:
		SensoriArray[j]["name"] = cgi.escape(form[NameN].value)
	FilenameN = "filename"+str(j)
	if FilenameN not in form:
		print("<br/>Errore:", FilenameN)
		Error = FilenameN
	else:
		if os.path.exists(str(Dir1wire)+str(cgi.escape(form[FilenameN].value))):
			SensoriArray[j]["filename"] = cgi.escape(form[FilenameN].value)
		else:
			Error = cgi.escape(form[FilenameN].value)+"- NON ESISTE"

# Cerco i sensori nel file json, ma stavolta per fare il contrario, scriverli
for i in range(len(ConfigFile)):
	if "sensori" == (ConfigFile[i]["name"]):
		# Appoggio a variabile l'array
		ConfigFile[i]["value"] = SensoriArray

# Se non c'e` stato nessun errore, apro e scrivo il file
if Error == "":
	with open("config.json", "w") as outfile:
		# Stampo a video la matrice se viene validata e inserita
		print("""
			<br/>
			<h4>Dati correttamente inseriti</h4>
			<br/>
			<p>Questo e` il risultato dell'insterimento:</p>
		""")
		print(SensoriArray)
		print(ConfigFile)
		json.dump(ConfigFile, outfile, indent=4)
else:
	print("<h2>Errore</h2>")
	print("<p>",Error,"</p>")


# End body/End html
print("""
</body>
</html>
""")
