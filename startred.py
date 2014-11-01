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

Ho spostato il ricalcolo dei tempi di ciclo dopo le operazioni,
cioe` ogni volta che vene azzerato un calcolo tempo.
Nel mezzo del while true veniva eseguito troppo spesso e modificando
il config.json lo script va in crash.

Risolvere il problem facendo "ricalcolare" le variabili solo al
cambio files di configurazione o su esplicito comando operatore.
Poi servira` anche un controllo che lo script e` in funzione e
magari qualcosa per poterlo riavviare.

"""

import time
import os
import json
import RPi.GPIO as GPIO

# Nota: GPIO.BOARD utilizza il "connettore pin numero"
# Per esempio, per usare il GPIO22 si deve specificare il pin 15: GPIO.setup(15, GPIO.OUT)
GPIO.setmode(GPIO.BOARD)



## Probabilmente questi file saranno da leggere in una funzione
# Provo a lasciarli qua, separati
#if os.path.exists("config.json"):
#	with open("config.json") as JsonFileConfig:
#		ConfigFile = json.load(JsonFileConfig)
#else:
#	print ("Errore, manca il file \"config.json\"")

#if os.path.exists("setpointarray.json"):
#	with open("setpointarray.json") as JsonFileSetPoints:
#		SetPoints = json.load(JsonFileSetPoints)
#else:
#	print ("Errore, manca il file \"setpointarray.json\"")

#if os.path.exists("dayssetpointarray.json"):
#	with open("dayssetpointarray.json") as JsonFileDays:
#		DaysSetPoints = json.load(JsonFileDays)
#else:
#	print ("Errore, manca il file \"daysetpointarray.json\"")

#if os.path.exists("temperature.csv"):
#	FileTempsCSV = open("temperature.csv","a")
#else:
#	print ("Errore, manca il file \"temperature.csv\"")

def CalcolaTempiCiclo():
	if os.path.exists("config.json"):
		with open("config.json") as JsonFileConfig:
			ConfigFile = json.load(JsonFileConfig)
			JsonFileConfig.close()
	else:
		print ("Errore, manca il file \"config.json\"")
	
	# Cerco ..
	for i in range(len(ConfigFile)):
		if "minutecycle" == (ConfigFile[i]["name"]):
			TempoCiclo = int(ConfigFile[i]["value"])*60	# Trasformo subito in secondi
	for i in range(len(ConfigFile)):
		if "minutegraph" == (ConfigFile[i]["name"]):
			TempoGraph = int(ConfigFile[i]["value"])*60	# Trasformo subito in secondi
	return TempoCiclo,TempoGraph

def CalcolaUscitaTermostato():
	if os.path.exists("config.json"):
		with open("config.json") as JsonFileConfig:
			ConfigFile = json.load(JsonFileConfig)
			JsonFileConfig.close()
	else:
		print ("Errore, manca il file \"config.json\"")
	
	# Cerco ..
	for i in range(len(ConfigFile)):
		if "outgpio" == (ConfigFile[i]["name"]):
			UscitaTermostato = int(ConfigFile[i]["value"])	# Trasformo in tero
			return UscitaTermostato

def CalcolaTemperature():
	### TEMPERATURE.CSV
	if os.path.exists("config.json"):
		with open("config.json") as JsonFileConfig:
			ConfigFile = json.load(JsonFileConfig)
			JsonFileConfig.close()
	else:
		print ("Errore, manca il file \"config.json\"")
	
	if os.path.exists("setpointarray.json"):
		with open("setpointarray.json") as JsonFileSetPoints:
			SetPoints = json.load(JsonFileSetPoints)
			JsonFileSetPoints.close()
	else:
		print ("Errore, manca il file \"setpointarray.json\"")
	
	if os.path.exists("dayssetpointarray.json"):
		with open("dayssetpointarray.json") as JsonFileDays:
			DaysSetPoints = json.load(JsonFileDays)
			JsonFileDays.close()
	else:
		print ("Errore, manca il file \"daysetpointarray.json\"")
	if os.path.exists("temperature.csv"):
		FileTempsCSV = open("temperature.csv","a")
	else:
		print ("Errore, manca il file \"temperature.csv\"")
	
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
	return TemperaturaTermostato,SetPoint

#### PROGRAMMA
# Ho aggiunto try+except per pulire la GPIO quanto interrompo con CTRL+C
TemperaturePID = CalcolaTemperature()	# Calcola le temperature per il PID ed aggiorna temperature.csv
TempoInizio= [int(time.time()),int(time.time())]	# TempiInizio, sono uguali ;)
# TempiCiclo[0] = ciclo, [1] = grafico | Secondi
TempiCiclo = CalcolaTempiCiclo()
try:
	while True:
		if int(time.time())-TempoInizio[0] > TempiCiclo[0]:
			# Set uscite termostato per comando
			UscitaTermostato = CalcolaUscitaTermostato()
			#print(type(UscitaTermostato))	# Per controllare fosse un intero
			GPIO.setup(UscitaTermostato, GPIO.OUT)
			
			if int(TemperaturePID[1]) > int(TemperaturePID[0]):
				print("Accendi uscita",UscitaTermostato)
				GPIO.output(UscitaTermostato, True)
			else:
				print("Spegni uscita",UscitaTermostato)
				GPIO.output(UscitaTermostato, False)
			TempoInizio[0] = int(time.time())
			print(TempiCiclo[0],"secondi ciclo")
			# TempiCiclo[0] = ciclo, [1] = grafico | Secondi
			TempiCiclo = CalcolaTempiCiclo()
		
		if int(time.time())-TempoInizio[1] > TempiCiclo[1]:
			# Temperature PID [0] = Termostato, [1] = SetPoint
			TemperaturePID = CalcolaTemperature()	# Calcola le temperature per il PID ed aggiorna temperature.csv
			print("TemperaturaTermostato:",TemperaturePID[0])
			print("SetPoint:",TemperaturePID[1])
			TempoInizio[1] = int(time.time())
			print(TempiCiclo[1],"secondi graph")
			# TempiCiclo[0] = ciclo, [1] = grafico | Secondi
			TempiCiclo = CalcolaTempiCiclo()
except KeyboardInterrupt:
	GPIO.cleanup()
