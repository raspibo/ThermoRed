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
<h2>Configurazione sensori temperatura</h2>
<p><b>ATTENZIONE</b>:</p>
<ul>
<li>Descrizione del sensore</li>
    <ul>
    <li>Non utilizzare caratteri speciali, sembra impediscano la visualizzazione in alcuni casi
    (non ho provato se si tratta solo di un difetto di visualizzazione o se e` un problema,
    opterei per il fatto che sia anche un problema)</li>
    </ul>
</li>
<li>Identificativo</li>
    <ul>
    <li>Non utilizzare caratteri speciali, sembra impediscano la visualizzazione in alcuni casi
    (non ho provato se si tratta solo di un difetto di visualizzazione o se e` un problema,
    opterei per il fatto che sia anche un problema)</li>
    </ul>
</li>
</ul>
<br/>
<br/>
""")

# Cerco la directory dei device 1 wire
for i in range(len(ConfigFile)):
	if "dir1w" == (ConfigFile[i]["name"]):
		# Appoggio a variabile
		Dir1wire = os.listdir(ConfigFile[i]["value"])
		Dir1wire.remove("w1_bus_master1")

# Stampo sulla pagina web il listato della directory dei sensori 1wire
# teoricamente e` da togliere sempre l'ultimo risultato,
# suggerisco di lasciarlo visibile, tanto non dovrebbe infastidire.
print("<h3>Sensori trovati (e` un semplice listato della directory):</h3>")
for i in range(len(Dir1wire)):
	print("<ul>")
	print("<li>",Dir1wire[i],"</li>")
	print("</ul>")

print("<p><hr/></p><br/>")	# Stampa un linea orizzontale

# Cerco i sensori nel file json
for i in range(len(ConfigFile)):
	if "sensori" == (ConfigFile[i]["name"]):
		# Appoggio a variabile l'array
		SensoriArray = ConfigFile[i]["value"]

# Start FORM input
# write*.py
print("<form action=\"/cgi-bin/writesensors.py\" method=\"post\">")
print("<table>")

# Per tutti i sensori presenti
for i in range(len(SensoriArray)):
	print("<tr><td>Descrizione del sensore:</td><td><input type=\"text\" name=\"display",i,"\" value=\"",SensoriArray[i]["display"],"\" size=\"40\" required></td></tr>", sep="")
	print("<tr><td>Identificativo:</td><td><input type=\"text\" name=\"name",i,"\" value=\"",SensoriArray[i]["name"],"\" size=\"40\" required></td></tr>", sep="")
	print("<tr><td>Filename:</td><td><select name=\"value",i,"\">", sep="")
	for j in range(len(Dir1wire)):
		if SensoriArray[i]["value"] == Dir1wire[j]:
			Selected="selected"
		else:
			Selected=""
		print("<option value=\"",Dir1wire[j],"\"",Selected,">",Dir1wire[j],"</option>", sep="")
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
