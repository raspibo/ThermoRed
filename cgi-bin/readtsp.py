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
<h2>Configurazione temperature Set Points</h2>
<p><b>ATTENZIONE</b>:</p>
<p>Accetta solo valori (numeri) interi.</p>
<p>Numeri da 5 (min) a 30 (max).</p>
<br/>
<br/>
""")


print("<p><hr/></p><br/>")	# Stampa un linea orizzontale

# Cerco ..
for i in range(len(ConfigFile)):
	if "temperature" == (ConfigFile[i]["name"]):
		# Appoggio a variabile l'array
		TempsArray = ConfigFile[i]["value"]


# Start FORM input
# write*.py
print("<form action=\"/cgi-bin/writetsp.py\" method=\"post\">")
print("<table>")

# Per tutta la lunghezza/voci contenute nell'array ..
for i in range(len(TempsArray)):
	# Concatenamento di variabili da SetPoins e pezzi di html
	print("<tr><td>",TempsArray[i]["display"],":</td><td><input type=\"number\" name=\"",TempsArray[i]["name"],"\" value=\"",TempsArray[i]["value"],"\" min=\"5\" max=\"30\" maxlength=\"2\" size=\"2\" required><br/></td></tr>", sep="")

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
