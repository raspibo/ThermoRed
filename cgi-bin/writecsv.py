#!/usr/bin/env python3

# Copia files nel .bak

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

def SearchDisplayJsonVar(JsonVar,SearchName):
	for i in range(len(JsonVar)):
		if SearchName == JsonVar[i]["name"]:
			return JsonVar[i]["display"]

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

# Cerco ...
for i in range(len(ConfigFile)):
	if "graph" == (ConfigFile[i]["name"]):
		# Appoggio a variabile l'array
		GraphArray = ConfigFile[i]["value"]

# Apro il file in scrittura
FileTemp = open("temperature.csv","w")

# Cerco e ..
FileTemp.write(SearchDisplayJsonVar(GraphArray,"data"))
FileTemp.write(",")
#FileTemp.write(SearchDisplayJsonVar(GraphArray,"var"))
#FileTemp.write(",")
#FileTemp.write(SearchDisplayJsonVar(GraphArray,"var"))
#FileTemp.write(",")
for i in range(len(GraphArray)):
	if "var" == (GraphArray[i]["name"]):
		# Appoggio a variabile l'array
		FileTemp.write(GraphArray[i]["display"])
		FileTemp.write(",")
FileTemp.write(SearchDisplayJsonVar(GraphArray,"setpoint"))
FileTemp.write('\n')
FileTemp.close()

FileTemp = open("temperature.csv","r")
FileCSV = FileTemp.read()
FileTemp.close()
print("Azzeramento eseguito, questo e` il contenuto del file \"temperature.csv\":<br/>")
print(FileCSV)
# Chiudo il file

# End body/End html
print("""
</body>
</html>
""")
