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
<h2>Configurazione GPIO "utili" del Raspberry Pi</h2>
<p><b>ATTENZIONE</b>:</p>
<p>Al momento sono previsti i pin della sola versione "B" e non legati ad altre funzionalita` (almeno spero ;))</p>
<p><b>Inserisci i numeri della GPIO separati da una virgola ","</b></p>
<br/>
<br/>
""")

print("<p><hr/></p><br/>")	# Stampa un linea orizzontale

# Start form input
print("<form action=\"/cgi-bin/writerpigpio.py\" method=\"post\">")
print("<table>")

# Cerco il dato che mi serve ..
for i in range(len(ConfigFile)):
	if "outfreegpio" == (ConfigFile[i]["name"]):
		# Genero la pagina di input
		print("<tr><td>",ConfigFile[i]["display"],":</td><td><input type=\"text\" name=\"",ConfigFile[i]["name"],"\" value=\"",ConfigFile[i]["value"],"\" size=\"40\" required><br/></td></tr>", sep="")

print("<td></td><td><input type=\"submit\" value=\"Submit\"></td>")
print("</table>")
print("</form>")	# END form


# End body/End html
print("""
</body>
</html>
""")
