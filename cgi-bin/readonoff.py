#!/usr/bin/env python3

# Questo file legge il file di configurazione,
# trova e modifica il parametro eseguendo il rispettivo "write*.py"

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
<h2>Configurazione funzionamento</h2>
<p>on / off / manuale</p>
<br/>
<br/>
""")


print("<p><hr/></p><br/>")	# Stampa un linea orizzontale


# Start FORM input
# write*.py
print("<form action=\"/cgi-bin/writeonoff.py\" method=\"post\">")
print("<table>")

print("<tr><td>Selezione della modalita` di funzionamento:</td>")	# Questa e` una riga di tabella in piu` con una linea

# Ricerca ...
for i in range(len(ConfigFile)):
	if "on" == (ConfigFile[i]["name"]):
		# Una volta trovato inizo ad |impostare" la form
		print("<td><select name=\"on\">")
		for j in ['on','man','off']:
			# Controllo il valore preimpostato e setto/resetto la selezione
			if ConfigFile[i]["value"] == j:
				Selected="selected"
			else:
				Selected=""
			print("<option value=\"",j,"\"",Selected,">",j,"</option>", sep="")
		print("</select></td></tr>")


print("<tr><td colspan=\"2\"><hr/></td></tr>")	# Questa e` una riga di tabella in piu` con una linea

print("<tr>")
print("<td></td><td><input type=\"submit\" value=\"Submit\"></td>")
print("</tr>")
print("</table>")
print("</form>")	# END form


# End body/End html
print("""
</body>
</html>
""")
