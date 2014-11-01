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
<h2>Configurazione del grafico delle temperature</h2>
<p><b>ATTENZIONE</b>:</p>
<p>Tutti i valori non hanno importanza (per ora).</p>
<p>Hanno importanza le descrizioni, che sono quelle che compaiono nel grafico delle temperature e gli <b>identificativi</b>, che vengono utilizzati per la ricerca</p>
<p>Questa e` una di quelle pagine che dovra` essere rivista perche` deve avere la possbibilita` di aggiungere e togliere dati, coordinatamente al file "temperature.csv"
(che deve essere archiviato/salvato e poi rigenerato)</p>
<p>Lunga storia ... per ora limitiamoci a due sonde ... o una, poi vedo come fare ..</p>
<p>Aggiunto "hidden" ai valori non modificabili</p>
<p>Non potevo mischiare le impostazioni a meno di rivoluzionare il tutto, quindi ho optato per l'inserimento manuale delle sonde di temperatura</p>

<br/>
<br/>
""")

print("<h3>Lista dei sensori trovati/inseriti</h3>")
for i in range(len(ConfigFile)):
	if "sensori" == (ConfigFile[i]["name"]):
		# Appoggio a variabile l'array
		SensoriArray = ConfigFile[i]["value"]
for j in range(len(SensoriArray)):
	print(SensoriArray[j]["display"],": <b>",SensoriArray[j]["name"],"</b><br/>", sep="")


print("<p><hr/></p><br/>")	# Stampa un linea orizzontale

# Cerco i valori nel file json
for i in range(len(ConfigFile)):
	if "graph" == (ConfigFile[i]["name"]):
		# Appoggio a variabile l'array
		GraphArray = ConfigFile[i]["value"]

# Start FORM input
# writesensors.py
print("<form action=\"/cgi-bin/writegraph.py\" method=\"post\">")
print("<table>")

# Ricerca ..
for j in range(len(GraphArray)):
	print("<tr><td>Descrizione del valore:</td><td><input type=\"text\" name=\"display",j,"\" value=\"",GraphArray[j]["display"],"\" size=\"40\" </td></tr>", sep="")
	print("<tr><td>Identificativo:</td><td><input type=\"text\" name=\"name",j,"\" value=\"",GraphArray[j]["name"],"\" size=\"40\" </td></tr>", sep="")
	print("<tr><td hidden>Valore:</td><td hidden><input type=\"text\" name=\"value",j,"\" value=\"",GraphArray[j]["value"],"\" size=\"40\" </td></tr>", sep="")
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
