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
<h2>Configurazione parametri PID</h2>
<p><b>ATTENZIONE</b>:</p>
<ul>
<li>
    La frequenza di controllo e` espressa in minuti, puo` andare da 1 a 60
</li>
<li>
    La temperatura di approssimazione e` espressa in decimi di grado, puo` andare da 0 a 10, quindi un grado massimo.
</li>
<li>
    Il sensore termostato e` quello di riferimento per il PID
</li>
<li>
    L'uscita e` quella che comanda il riscaldamento
</li>
</ul>
<p><h4>Temperature</h4>
Informazioni per le impostazioni di temperature inerziali positive e negative.
Teoricamente, piu` e` lungo il tempo di ciclo del PID piu` bassi devono essere i valori d'inerzia.
Ovviamente sono due variabili (tempi e inerzie) da "sperimentare", per arrivare ad una configurazione soddisfacente,
per non accendere/spegnere continuamente, pur mantenendo una temperatura il piu` possibile costante.
</p>
<p>
<pre>
Inerzia sopra +: --------------------------- Se Letta + Sopra > Set Point = Out OFF
Set Point      : ===========================
Inerzia sotto -: --------------------------- Se Letta + Sotto < Set Point = Out ON
</pre>
</p>
<br/>
<br/>
""")


print("<p><hr/></p><br/>")	# Stampa un linea orizzontale

# Cerco ..
for i in range(len(ConfigFile)):
	if "pid" == (ConfigFile[i]["name"]):
		# Appoggio a variabile l'array
		PidArray = ConfigFile[i]["value"]

for i in range(len(ConfigFile)):
	if "sensori" == (ConfigFile[i]["name"]):
		# Appoggio a variabile l'array
		SensoriArray = ConfigFile[i]["value"]

for i in range(len(ConfigFile)):
	if "outs" == (ConfigFile[i]["name"]):
		# Appoggio a variabile l'array
		OutsArray = ConfigFile[i]["value"]


# Start FORM input
# write*.py
print("<form action=\"/cgi-bin/writepid.py\" method=\"post\">")
print("<table>")


for i in range(len(PidArray)):
	print("<tr><td>Descrizione:</td><td><input type=\"text\" name=\"display",i,"\" value=\"",PidArray[i]["display"],"\" size=\"40\" required readonly></td></tr>", sep="")
	print("<tr><td>Nome:</td><td><input type=\"text\" name=\"name",i,"\" value=\"",PidArray[i]["name"],"\" size=\"40\" required readonly></td></tr>", sep="")
	#print("<tr><td>Valore:</td><td><input type=\"text\" name=\"value",i,"\" value=\"",PidArray[i]["value"],"\" size=\"40\" required readonly></td></tr>", sep="")
	if "minutecycle" == PidArray[i]["name"]:
		print("<tr><td>Valore (minuti):</td><td><input type=\"number\" name=\"value",i,"\" value=\"",PidArray[i]["value"],"\" min=\"1\" max=\"60\" maxlength=\"2\" size=\"2\" required></td></tr>", sep="")
	elif "tempcycle+" == PidArray[i]["name"]:
		print("<tr><td>Valore (decimi di grado):</td><td><input type=\"number\" name=\"value",i,"\" value=\"",PidArray[i]["value"],"\" min=\"0\" max=\"10\" maxlength=\"2\" size=\"2\" required></td></tr>", sep="")
	elif "tempcycle-" == PidArray[i]["name"]:
		print("<tr><td>Valore (decimi di grado):</td><td><input type=\"number\" name=\"value",i,"\" value=\"",PidArray[i]["value"],"\" min=\"-10\" max=\"0\" maxlength=\"2\" size=\"2\" required></td></tr>", sep="")
	elif "termostato" == PidArray[i]["name"]:
		print("<tr><td>Valore:</td><td><select name=\"value",i,"\">", sep="")
		for j in range(len(SensoriArray)):
			if SensoriArray[j]["name"] == PidArray[i]["value"]:
				Selected="selected"
			else:
				Selected=""
			print("<option value=\"",SensoriArray[j]["name"],"\"",Selected,">",SensoriArray[j]["display"],"</option>", sep="")
		print("</select></td></tr>")
	elif "outterm" == PidArray[i]["name"]:
		print("<tr><td>Valore:</td><td><select name=\"value",i,"\">", sep="")
		for j in range(len(OutsArray)):
			if OutsArray[j]["name"] == PidArray[i]["value"]:
				Selected="selected"
			else:
				Selected=""
			print("<option value=\"",OutsArray[j]["name"],"\"",Selected,">",OutsArray[j]["display"],"</option>", sep="")
		print("</select></td></tr>")
	else:
		print("C'e` un problema")

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
