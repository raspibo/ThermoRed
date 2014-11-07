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
<h2>Configurazione uscite GPIO Raspberry Pi</h2>
<p><b>ATTENZIONE</b>:</p>
<ul>
<li>Descrizione uscita</li>
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
<li>Pin</li>
    <ul>
    <li></li>
    </ul>
</li>
</ul>
<br/>
<br/>
""")


print("<p><hr/></p><br/>")	# Stampa un linea orizzontale

# Cerco ..
for i in range(len(ConfigFile)):
	if "outs" == (ConfigFile[i]["name"]):
		# Appoggio a variabile l'array
		OutsArray = ConfigFile[i]["value"]

for i in range(len(ConfigFile)):
	if "outfreegpio" == (ConfigFile[i]["name"]):
		OutsFree = ConfigFile[i]["value"]

# Start FORM input
# write*.py
print("<form action=\"/cgi-bin/writeoutgpio.py\" method=\"post\">")
print("<table>")

# ..
for j in range(len(OutsArray)):
	print("<tr><td>Descrizione dell'uscita:</td><td><input type=\"text\" name=\"display",j,"\" value=\"",OutsArray[j]["display"],"\" size=\"40\" required></td></tr>", sep="")
	print("<tr><td>Identificativo:</td><td><input type=\"text\" name=\"name",j,"\" value=\"",OutsArray[j]["name"],"\" size=\"40\" required></td></tr>", sep="")
	print("<tr><td>Pin (GPIO):</td><td><select name=\"value",j,"\">", sep="")
	for k in OutsFree.split(","):	# .split() converte una stringa in lista, fra parentesi il separatore (la virgola)
		print(k)
		# Controllo il valore preimpostato e setto/resetto la selezione
		if k == OutsArray[j]["value"]:
			Selected="selected"
		else:
			Selected=""
		print("<option value=\"",k,"\"",Selected,">",k,"</option>", sep="")
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
