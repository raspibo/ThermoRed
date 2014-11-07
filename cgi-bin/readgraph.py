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
<h2>Configurazione grafico temperature</h2>
<p><b>ATTENZIONE</b>:</p>
<p>Ne faccio un pezzetto alla volta..</p>
<p>Prima il refresh</p>
<p>Comunque e` altamente probabile che debba farne due .. o tre</p>
<br/>
<br/>
""")


print("<p><hr/></p><br/>")	# Stampa un linea orizzontale

# Cerco ..
for i in range(len(ConfigFile)):
	if "graph" == (ConfigFile[i]["name"]):
		# Appoggio a variabile l'array
		GraphArray = ConfigFile[i]["value"]

for i in range(len(ConfigFile)):
	if "sensori" == (ConfigFile[i]["name"]):
		# Appoggio a variabile l'array
		SensoriArray = ConfigFile[i]["value"]


# Start FORM input
# write*.py
print("<form action=\"/cgi-bin/writegraph.py\" method=\"post\">")
print("<table>")

# Per tutta la lunghezza/voci contenute nell'array ..
#for i in range(len(GraphArray)):
#	# Concatenamento di variabili da SetPoins e pezzi di html
#	print("<tr><td>",GraphArray[i]["display"],":</td><td><input type=\"number\" name=\"",GraphArray[i]["name"],"\" value=\"",GraphArray[i]["value"],"\" min=\"5\" max=\"30\" maxlength=\"2\" size=\"2\" required><br/></td></tr>", sep="")
#for i in range(len(ConfigFile)):
#	if "minutegraph" == (ConfigFile[i]["name"]):
#		print("<tr><td>",ConfigFile[i]["display"],":</td><td><input type=\"number\" name=\"",ConfigFile[i]["name"],"\" value=\"",ConfigFile[i]["value"],"\" min=\"1\" max=\"60\" maxlength=\"2\" size=\"2\" required><br/></td></tr>", sep="")

#print("<tr><td colspan=\"2\"><hr/></td></tr>")	# Questa e` una riga di tabella in piu` con una linea

for i in range(len(GraphArray)):
	if "minutegraph" == GraphArray[i]["name"]:
		Disable = "readonly"
	else:
		Disable = ""
	print("<tr><td>Descrizione:</td><td><input type=\"text\" name=\"display",i,"\" value=\"",GraphArray[i]["display"],"\" size=\"40\" required ",Disable,"></td></tr>", sep="")
	#print("<tr><td>Identificazione:</td><td><input type=\"text\" name=\"name",i,"\" value=\"",GraphArray[i]["name"],"\" size=\"40\" required ",Disable,"></td></tr>", sep="")
	#print("<tr><td>Valore:</td><td><input type=\"text\" name=\"value",i,"\" value=\"",GraphArray[i]["value"],"\" size=\"40\" required ",Disable,"></td></tr>", sep="")
	if "fixed" == GraphArray[i]["value"]:
		print("<tr><td>Nome:</td><td><input type=\"text\" name=\"name",i,"\" value=\"",GraphArray[i]["name"],"\" size=\"40\" readonly></td></tr>", sep="")
		print("<tr><td>Valore:</td><td><input type=\"text\" name=\"value",i,"\" value=\"",GraphArray[i]["value"],"\" size=\"40\" readonly></td></tr>", sep="")
	elif Disable != "":
		print("<tr><td>Nome:</td><td><input type=\"text\" name=\"name",i,"\" value=\"",GraphArray[i]["name"],"\" size=\"40\" readonly></td></tr>", sep="")
		print("<tr><td>Valore:</td><td><input type=\"number\" name=\"value",i,"\" value=\"",GraphArray[i]["value"],"\" min=\"1\" max=\"60\" maxlength=\"2\" size=\"2\" required></td></tr>", sep="")
	else:
		print("<tr><td>Valore:</td><td><input type=\"text\" name=\"value",i,"\" value=\"",GraphArray[i]["value"],"\" size=\"40\" readonly></td></tr>", sep="")
		#print("<tr><td>Valore:</td><td><input type=\"number\" name=\"value",i,"\" value=\"",GraphArray[i]["value"],"\" readonly></td></tr>", sep="")
		print("<tr><td>Nome:</td><td><select name=\"name",i,"\">", sep="")
		for j in range(len(SensoriArray)):
			if SensoriArray[j]["name"] == GraphArray[i]["name"]:
				Selected="selected"
			else:
				Selected=""
			print("<option value=\"",SensoriArray[j]["name"],"\"",Selected,">",SensoriArray[j]["name"],"</option>", sep="")
			#print("<tr><td>Valore:</td><td><input type=\"text\" name=\"value",i,"\" value=\"",GraphArray[i]["value"],"\" size=\"40\" disabled></td></tr>", sep="")
	print("</select></td></tr>")
	print("<tr><td colspan=\"2\"><hr/></td></tr>")	# Questa e` una riga di tabella in piu` con una linea

#print("<tr><td colspan=\"2\"><hr/></td></tr>")	# Questa e` una riga di tabella in piu` con una linea



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
