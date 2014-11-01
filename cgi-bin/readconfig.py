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
<h2>Visualizza file di configurazione "config.json"</h2>
<p><b>ATTENZIONE</b>:</p>
<p>Questa pagina prende in input il file di configurazione json, non e` possibile effettuare modifiche, e` bloccata, per ovvi motivi</p>
<br/>
<br/>
""")

print("<p><hr/></p><br/>")	# Stampa un linea orizzontale

# Start FORM input
# writesensors.py
print("<form action=\"/cgi-bin/writejson.py\" method=\"post\">")
print("<table>")

# Per tutte le voci presenti ..
for j in range(len(ConfigFile)):
	print("<tr><td>Descrizione:</td><td><input type=\"text\" name=\"display",j,"\" value=\"",ConfigFile[j]["display"],"\" size=\"40\" </td></tr>", sep="")
	print("<tr><td>Nome identificativo:</td><td><input type=\"text\" name=\"name",j,"\" value=\"",ConfigFile[j]["name"],"\" size=\"20\" </td></tr>", sep="")
	print("<tr><td>Valore:</td><td><input type=\"text\" name=\"filename",j,"\" value=\"",ConfigFile[j]["value"],"\" size=\"75\" </td></tr>", sep="")
	print("<tr><td colspan=\"2\"><hr/></td></tr>")	# Questa e` una riga di tabella in piu` con una linea


print("<tr><td colspan=\"2\"><hr/></td></tr>")	# Solita linea di separazione (forse si potrebbe farne a meno)
print("<tr>")
#print("<td></td><td><input type=\"submit\" value=\"Submit\"></td>")
print("</tr>")
print("</table>")
print("</form>")	# END form


# End body/End html
print("""
</body>
</html>
""")
