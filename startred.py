#!/usr/bin/env python3

""" Note di programmazione
- Lo script non si deve mai fermare, deve agire in conseguenza dei
dati impostati nel "config.json"
- Servira` una funzione per la rilettura dei dati, il come, quando e perche`
e` tutto da vedere
- Che varabili serviranno ?
	Per il temperature.csv:
		Data
		Sensore Temperatura
		Secondo Sensore
		Set Point
	Per il comando dell'uscita:
		L'uscita
		Il sensore di rieferimento della temperatura da controllare
	La frequenza di controllo servira` per tutto ?
		Per il grafico, quindi temperature.csv
		Per il PID, quindi il comando dell'uscita
	Necessitera` sapere se l'impianto e`: ON, Manuale, Off.
	Questo perche` cambieranno i set point da automatico a manuale,
	o perche` dovro` interrompere il comando dell'uscita.
- Conviene mettere tutte le variabili in gruppo, o conviene singole ?
	Per semplicita` mi suggerisco singole ;)
"""

import time
import os
import json

## Probabilmente questi file saranno da leggere in una funzione
if os.path.exists("config.json"):
	with open("config.json") as JsonFileConfig:
		ConfigFile = json.load(JsonFileConfig)
else:
	print ("Errore, manca il file \"config.json\"")

if os.path.exists("setpointarray.json"):
	with open("setpointarray.json") as JsonFileSetPoints:
		SetPoints = json.load(JsonFileSetPoints)
else:
	print ("Errore, manca il file \"setpointarray.json\"")

if os.path.exists("dayssetpointarray.json"):
	with open("dayssetpointarray.json") as JsonFileDays:
		DaysSetPoints = json.load(JsonFileDays)
else:
	print ("Errore, manca il file \"daysetpointarray.json\"")

if os.path.exists("temperature.csv"):
	FileTempsCSV = open("temperature.csv","a")
else:
	print ("Errore, manca il file \"temperature.csv\"")


### TEMPERATURE.CSV

## Cerco i sensori

# Filename
EndFilename = "w1_slave"

# Directory
for i in range(len(ConfigFile)):
	if "dir1w" == (ConfigFile[i]["name"]):
		DirSensors = ConfigFile[i]["value"]

# Sensori array
for i in range(len(ConfigFile)):
	if "sensori" == (ConfigFile[i]["name"]):
		# Appoggio a variabile l'array
		SensoriArray = ConfigFile[i]["value"]

## Scrittura "temperature.csv"
FileTempsCSV.write(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))
# Aggiungo la virgola di separazione
FileTempsCSV.write(',')

# Cerco il termostato di riferimento
for i in range(len(ConfigFile)):
	if "termostato" == (ConfigFile[i]["name"]):
		# Cerco i sensori
		for j in range(len(SensoriArray)):
			# Se e` il termostato
			if SensoriArray[j]["name"] == ConfigFile[i]["value"]:
				FileTermostato = SensoriArray[j]["filename"]
				Termostato = open(DirSensors+FileTermostato+"/"+EndFilename,"r")
				# Controlla se gli ultimi caratteri della stringa letta sono uguali a
				if (Termostato.readline()[-4:-1]) == "YES":
					# Effettuo il calcolo della temperatura indicando che il valore e` intero
					# prima del calcolo e che e` una stringa per passarla in scrittura
					# Mi serve il valore per il confronto ed il comando dell'uscita
					TemperaturaTermostato=int(Termostato.readline()[-6:-1])/1000	# Qui nasce la variabile TermeraturaTermostato ****
					FileTempsCSV.write(str(TemperaturaTermostato))
				else:
					FileTempsCSV.write('err')	# err, se errore sonda, non so ancora cosa fara` il grafico perche` non e` successo.
				# Aggiungo la virgola di separazione
				FileTempsCSV.write(',')

# Tutti gli altri ..
for i in range(len(ConfigFile)):
	if "termostato" == (ConfigFile[i]["name"]):
		# Cerco i sensori
		for j in range(len(SensoriArray)):
			# Se non e` il termostato
			if SensoriArray[j]["name"] != ConfigFile[i]["value"]:
				FileSensore = SensoriArray[j]["filename"]
				Sensore = open(DirSensors+FileSensore+"/"+EndFilename,"r")
				# Controlla se gli ultimi caratteri della stringa letta sono uguali a
				if (Sensore.readline()[-4:-1]) == "YES":
					# Effettuo il calcolo della temperatura indicando che il valore e` intero
					# prima del calcolo e che e` una stringa per passarla in scrittura
					# Mi serve il valore per il confronto ed il comando dell'uscita
					TemperaturaLetta=int(Sensore.readline()[-6:-1])/1000
					FileTempsCSV.write(str(TemperaturaLetta))
				else:
					FileTempsCSV.write('err')	# err, se errore sonda, non so ancora cosa fara` il grafico perche` non e` successo.
				# Aggiungo la virgola di separazione
				FileTempsCSV.write(',')

## SetPoint
# Prima devo "calcolare" il setpoint
Giorno=time.strftime("%w", time.localtime())
Ora=time.strftime("%H", time.localtime())
# 0 Domenica .. 6
if Giorno == "0":
	CalcoloGiorno="6"
else:
	CalcoloGiorno=int(Giorno)-1

# Puntatore giorno, ore, ora, temperatura
# nel file json
#print (DaysSetPoints[int(CalcoloGiorno)]["hours"][int(Ora)]["temperature"])
# Ricerca della temperatura nei files json
for i in range(len(SetPoints)):
	if (SetPoints[i]["name"]) == (DaysSetPoints[int(CalcoloGiorno)]["hours"][int(Ora)]["temperature"]):
		SetPoint = (SetPoints[i]["temperature"])

# Poi scrivo il setpoit richiesto
FileTempsCSV.write(SetPoint)

# Aggiungo il ritorno a capo di fine riga per i valori successivi
FileTempsCSV.write('\n')

FileTempsCSV.close()

### Inizio programma PID ###

# Questa e` la base
if float(SetPoint) > TemperaturaTermostato:
	print("Accendi l'uscita")
else:
	print("Spegni l'uscita")
