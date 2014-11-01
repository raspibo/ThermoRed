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
<h2>Configurazione sensore termostato</h2>
<p>E` quello utilizzato per determinare l'accensione e spegnimento del riscaldamento durante le funzioni automatiche.</p>
<p><b>ATTENZIONE</b>:</p>
<p>  </p>
<br/>
<br/>
""")

print("<p><hr/></p><br/>")	# Stampa un linea orizzontale

# Cerco i sensori disponibili nel file json
for i in range(len(ConfigFile)):
	if "sensori" == (ConfigFile[i]["name"]):
		# Appoggio a variabile l'array
		SensoriArray = ConfigFile[i]["value"]

# Start FORM input
# writesensors.py
print("<form action=\"/cgi-bin/writethermo.py\" method=\"post\">")
#print("<table>")

print("<p></p>")
print("Selezione sensore di riferimento PID: ")	# Questa e` una riga di tabella in piu` con una linea

# Cerco il termostato nel file config.json
for i in range(len(ConfigFile)):
	if "termostato" == (ConfigFile[i]["name"]):
		# Una volta trovato inizo ad |impostare" la form
		print("<select name=\"termostato\">")
		for j in range(len(SensoriArray)):
			# Controllo il valore preimpostato e setto/resetto la selezione
			if SensoriArray[j]["name"] == ConfigFile[i]["value"]:
				Selected="selected"
			else:
				Selected=""
			print("<option value=\"",SensoriArray[j]["name"],"\"",Selected,">",SensoriArray[j]["display"],"</option>", sep="")
		print("</select>")

print("<p></p>")
print("<input type=\"submit\" value=\"Submit\"></td>")
#print("</table>")
print("</form>")	# END form


# End body/End html
print("""
</body>
</html>
""")
