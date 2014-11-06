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
		Dir1wire = os.listdir(ConfigFile[i]["value"])


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
<p><b>ATTENZIONE</b>:</p>
<p>Meglio non utilizzare caratteri speciali, sembra impediscano la visualizzazione in alcuni casi
(non ho provato se si tratta solo di un difetto di visualizzazione o se e` un problema, opterei per il fatto che sia anche un problema)</p>
<br/>
<br/>
""")

# Stampo sulla pagina web il listato della directory dei sensori 1wire
# teoricamente e` da togliere sempre l'ultimo risultato,
# suggerisco di lasciarlo visibile, tanto non dovrebbe infastidire.
print("<h3>Sensori trovati (e` un semplice listato della directory):</h3>")
for i in range(len(Dir1wire)):
	print("<ul><li>",Dir1wire[i],"</li></ul>")

print("<p><hr/></p><br/>")	# Stampa un linea orizzontale

# Cerco i sensori nel file json
for i in range(len(ConfigFile)):
	if "sensori" == (ConfigFile[i]["name"]):
		# Appoggio a variabile l'array
		SensoriArray = ConfigFile[i]["value"]

# Start FORM input
# writesensors.py
print("<form action=\"/cgi-bin/writesensors.py\" method=\"post\">")
print("<table>")

# Per tutti i sensori presenti
for j in range(len(SensoriArray)):
	print("<tr><td>Descrizione del sensore:</td><td><input type=\"text\" name=\"display",j,"\" value=\"",SensoriArray[j]["display"],"\" size=\"40\" </td></tr>", sep="")
	print("<tr><td>Identificativo:</td><td><input type=\"text\" name=\"name",j,"\" value=\"",SensoriArray[j]["name"],"\" size=\"40\" </td></tr>", sep="")
	print("<tr><td>Filename:</td><td><input type=\"text\" name=\"filename",j,"\" value=\"",SensoriArray[j]["filename"],"\" size=\"40\" </td></tr>", sep="")
	print("<tr><td colspan=\"2\"><hr/></td></tr>")	# Questa e` una riga di tabella in piu` con una linea


print("<tr><td colspan=\"2\"><hr/></td></tr>")	# Solita linea di separazione (forse si potrebbe farne a meno)
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
