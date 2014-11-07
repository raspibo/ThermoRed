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
<h2>Configurazione pin d'uscita (GPIO) Raspberry Pi</h2>
<p><b>ATTENZIONE</b>:</p>
<p>Al momento sono previsti i pin della sola versione "B" e non legati ad altre funzionalita` (almeno spero ;))</p>
<p><b>Inserisci i numeri pin della board separati da una virgola ","</b></p>
<p>Non c'e` ancora la verifica sui dati inseriti.</p>
<p>Nota:<br/>
Il programma utilizzera` la modalita` GPIO.BOARD, che utilizza il "connettore pin numero",
per esempio, per usare il GPIO22 si deve specificare il pin 15: GPIO.setup(15, GPIO.OUT)
</p>
<p>
<a href="http://elinux.org/RPi_Low-level_peripherals" target="_blank">http://elinux.org/RPi_Low-level_peripherals</a>
</p>
<br/>
<br/>
""")


print("<p><hr/></p><br/>")	# Stampa un linea orizzontale


# Start FORM input
# write*.py
print("<form action=\"/cgi-bin/writerpigpio.py\" method=\"post\">")
print("<table>")

# Cerco ...
for i in range(len(ConfigFile)):
	if "outfreegpio" == (ConfigFile[i]["name"]):
		# Genero la pagina di input
		print("<tr><td>",ConfigFile[i]["display"],":</td><td><input type=\"text\" name=\"",ConfigFile[i]["name"],"\" value=\"",ConfigFile[i]["value"],"\" size=\"40\" required><br/></td></tr>", sep="")

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
