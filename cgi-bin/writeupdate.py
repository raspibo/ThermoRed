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
<h2>Configurazione frequenza di update</h2>
<p>E` la frequenza (in minuti) con cui si devono aggiornare e verificare i dati e comandare le uscite</p>
<p>  </p>
<br/>
<br/>
""")


form=cgi.FieldStorage()

Error = ""	# Serve per il calcolo/verifica di errore
# 
if "minutecycle" not in form:
	print("<br/>Errore: non hai inserito nessun dato?")
	Error = "Non hai inserito nessun dato ?"
else:
	# Cerco nel file config.json
	for i in range(len(ConfigFile)):
		if "minutecycle" == (ConfigFile[i]["name"]):
			# Una volta trovato ..
			ConfigFile[i]["value"] = cgi.escape(form[ConfigFile[i]["name"]].value)
		if "minutegraph" == (ConfigFile[i]["name"]):
			# Una volta trovato ..
			ConfigFile[i]["value"] = cgi.escape(form[ConfigFile[i]["name"]].value)

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
