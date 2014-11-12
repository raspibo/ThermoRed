#!/usr/bin/env python3

""" Vecchie note di programmazione (ho cambiato tutto o quasi)
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

###
Ho spostato il ricalcolo dei tempi di ciclo dopo le operazioni,
cioe` ogni volta che vene azzerato un calcolo tempo.
Nel mezzo del while true veniva eseguito troppo spesso e modificando
il config.json lo script va in crash.

Risolvere il problem facendo "ricalcolare" le variabili solo al
cambio files di configurazione o su esplicito comando operatore.
Poi servira` anche un controllo che lo script e` in funzione e
magari qualcosa per poterlo riavviare.

### Forse risolto il problema col "try"
### No. C'e` qualcos'altro.
### Messo una pezza col except ValueErrore e ritenta ..



"""

import time
import os
import json
import RPi.GPIO as GPIO

# Nota: GPIO.BOARD utilizza il "connettore pin numero"
# Per esempio, per usare il GPIO22 si deve specificare il pin 15: GPIO.setup(15, GPIO.OUT)
GPIO.setmode(GPIO.BOARD)

# Legge il file di configurazione
# Provo a generalizzarla
def ReadJsonFile(JsonFile):
	if os.path.exists(JsonFile):
		try:
			with open(JsonFile) as JsonFileOpen:
				JsonFileRead = json.load(JsonFileOpen)
				JsonFileOpen.close()
		except IOError:
			print ("Errore di I/O in lettura", JsonFile)
		except ValueError:
			print ("Errore dati", JsonFile," ritento ..")
			time.sleep(3)
			JsonFileRead = ReadJsonFile(JsonFile)	# Richiama se stessa
		else:
			return JsonFileRead
	else:
		print ("Arresto programma: manca il file", JsonFile)
		exit()

# Cerca qualcosa nella variabile Json
# Variabili da specificare:
# (1) Variabile Json
# (2) Ricerca
# (3) Campo di ricerca ("name"/"display"/"value")
# (4) Cosa si vuole leggere ("name"/"display"/"value")
# per esempio cerca "name"/"display"/"value", restituisci "name"/"display"/"value"
# Non credo mi servira` perche` dovrebbero essere tutte ricerche per nome
# con risultato valore (vedi SearchValueJsonVar)
def AllSearchJsonVar(JsonVar,SearchName,SearchType,ReadType):
	for i in range(len(JsonVar)):
		if SearchName == JsonVar[i][SearchType]:
			return JsonVar[i][ReadType]

# Cerca nella variabile Json, il valore di un "nome" specificato, restituisce il valore.
def SearchValueJsonVar(JsonVar,SearchName):
	for i in range(len(JsonVar)):
		if SearchName == JsonVar[i]["name"]:
			return JsonVar[i]["value"]

# Serve per cercare il risultato di un risultato
# utilizza la funzione SearchValueJsonVar(JsonVar,SearchName)
# Cerca il nome cha ha un valore array nella variabile Json,
# poi cerca il nome nell'array, restituisce il valore.
def SearchValue2JsonVar(JsonVar,SearchName1,SearchName2):
	for i in range(len(JsonVar)):
		if SearchName1 == JsonVar[i]["name"]:
			JsonVar2 = JsonVar[i]["value"]
			Results = SearchValueJsonVar(JsonVar2,SearchName2)
			return Results

# Restituisce [0] Giorno [1] Ora
def CalcolaGiornoOra():
	Giorno=time.strftime("%w", time.localtime())
	Ora=time.strftime("%H", time.localtime())
	# 0 Domenica .. 6
	if Giorno == "0":
		CalcoloGiorno="6"
	else:
		CalcoloGiorno=int(Giorno)-1
	return int(CalcoloGiorno),int(Ora)

# Aggiunge dati ad un file, aprendolo e richiudendolo
def AddFileData(Filename,Dato):
	if os.path.exists(Filename):
		FileTemp = open(Filename,"a")
		FileTemp.write(Dato)
		FileTemp.close()
	else:
		print ("Errore, manca il file", Filename)
		exit()


### Programma ###

# Mi serve un tempo d'inizio per l'aggiornamento Grafico e per il PID
# TempoInizio[0] grafico
# TempoInizio[1] pid
TempoInizio= [int(time.time()),int(time.time())]	# TempiInizio, sono uguali ;)
# Prima di tutto ..
ConfigFile = ReadJsonFile("config.json")
# Devo calcolare i tempi ciclo
# Grafico
#TempoGrafico = int(SearchValue2JsonVar(ConfigFile,"graph","minutegraph")*60)	# trasformo in secondi
TempoGrafico = 0
# Ciclo
#TempoCiclo = int(SearchValue2JsonVar(ConfigFile,"pid","minutecycle")*60)	# trasformo in secondi
TempoCiclo = 0
# Devo controllare/sapere almeno la temperatura PID e quella di setpoint
# servono per accendere spegnere l'uscita
#TempSetPoint = 

## Programma
try:
	while True:
		## Aggiorna il Grafico
		# Calcola/legge le temperature
		# Stampa su file
		if int(time.time()) - TempoInizio[0] > TempoGrafico:
			# Prima di tutto, guardo se .. manuale/on/off e setto una variabile
			EnableCycle = SearchValueJsonVar(ConfigFile,"on")
			print("Aggiornamento grafico")
			# Scrive il file temperature.csv
			# subito la data ..
			AddFileData("temperature.csv",time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))
			AddFileData("temperature.csv",",")
			# Legge e calcola le temperature
			# Cerco le sonde da visualizzare
			# prima la directory
			Dir1w = SearchValueJsonVar(ConfigFile,"dir1w")
			# il file di lettura e` fisso ? forse meglio inserire anche questo nel file conf.json
			EndFilename = SearchValueJsonVar(ConfigFile,"file1w")
			Sensori = SearchValueJsonVar(ConfigFile,"sensori")
			for i in range(len(Sensori)):
					Sensore = open(Dir1w+Sensori[i]["value"]+"/"+EndFilename,"r")
					# Controlla se gli ultimi caratteri della stringa letta sono uguali a
					if (Sensore.readline()[-4:-1]) == "YES":
						# Effettuo il calcolo della temperatura indicando che il valore e` intero
						# prima del calcolo e che e` una stringa per passarla in scrittura
						# Mi serve il valore per il confronto ed il comando dell'uscita
						TemperaturaLetta=int(Sensore.readline()[-6:-1])/1000
						print(TemperaturaLetta)
						AddFileData("temperature.csv",str(TemperaturaLetta))
					else:
						AddFileData("temperature.csv","err")	# err, se errore sonda, il grafico non visualizza (ok)
					# Aggiungo la virgola di separazione
					AddFileData("temperature.csv",",")
			# Calcola Temperatura Set Point
			# Se ciclo on .. calcola
			if EnableCycle == "on":
				TemperatureConf = SearchValueJsonVar(ConfigFile,"temperature")	# Temperature nel file di configurazione
				SetPoints = ReadJsonFile("weektsp.json")	# Temperature set point nel file week
				for i in range(len(TemperatureConf)):
					# Se il nome della temperatura nel file di configurazione
					# e` uguale al nome nel file week (posizione giorno, sottoposizione ora)
					if TemperatureConf[i]["name"] == SetPoints[CalcolaGiornoOra()[0]]["hours"][CalcolaGiornoOra()[1]]["temperature"]:
						TemperatureSetPoint = TemperatureConf[i]["value"]
						AddFileData("temperature.csv",str(TemperatureSetPoint))
			# .. altrimenti, trova e usa quella manuale
			elif EnableCycle == "man":
				TemperatureSetPoint = SearchValue2JsonVar(ConfigFile,"temperature","Tman")
				AddFileData("temperature.csv",str(TemperatureSetPoint))
			else:
				TemperatureSetPoint = SearchValue2JsonVar(ConfigFile,"temperature","Tice")	# Metto la piu` bassa (se non e` stata mal configurata)
				AddFileData("temperature.csv",str(TemperatureSetPoint))
			print(TemperatureSetPoint)
			AddFileData("temperature.csv","\n")	# Ho terminato ed aggiungo il ritorno a capo
			# Devo azzerare tempi e rileggere le variabili ..
			TempoInizio[0] = int(time.time())
			ConfigFile = ReadJsonFile("config.json")
			# Devo calcolare i tempi ciclo
			# Grafico
			TempoGrafico = int(SearchValue2JsonVar(ConfigFile,"graph","minutegraph"))*60	# trasformo in secondi
			# Ciclo
			TempoCiclo = int(SearchValue2JsonVar(ConfigFile,"pid","minutecycle"))*60	# trasformo in secondi
		
		## Comando uscita/Regolazione PID
		# Calcola la sonda di riferimento
		# Calcola l'uscita di riferimento
		# Confronta temperature +/- avvicinamento e decide
		if int(time.time()) - TempoInizio[1] > TempoCiclo:
			# Prima di tutto, guardo se .. manuale/on/off e setto una variabile
			EnableCycle = SearchValueJsonVar(ConfigFile,"on")
			print(EnableCycle)
			print("Aggiornamento ciclico")
			# Set uscite termostato per comando
			UscitaConfPID = SearchValue2JsonVar(ConfigFile,"pid","outterm")	# Cerco l'usicta configurate nel PID
			Uscite = SearchValueJsonVar(ConfigFile,"outs")	# Cerco le uscite disponibili
			for i in range(len(Uscite)):
				if UscitaConfPID == Uscite[i]["name"]:
					UscitaTermostato = int(Uscite[i]["value"])
			GPIO.setup(UscitaTermostato, GPIO.OUT)	# Set uscita
			# Calcola Temperatura Set Point
			# Se ciclo on .. calcola
			if EnableCycle == "on":
				TemperatureConf = SearchValueJsonVar(ConfigFile,"temperature")	# Temperature nel file di configurazione
				SetPoints = ReadJsonFile("weektsp.json")	# Temperature set point nel file week
				for i in range(len(TemperatureConf)):
					# Se il nome della temperatura nel file di configurazione
					# e` uguale al nome nel file week (posizione giorno, sottoposizione ora)
					if TemperatureConf[i]["name"] == SetPoints[CalcolaGiornoOra()[0]]["hours"][CalcolaGiornoOra()[1]]["temperature"]:
						TemperatureSetPoint = TemperatureConf[i]["value"]
			# .. altrimenti, trova e usa quella manuale
			elif EnableCycle == "man":
				TemperatureSetPoint = SearchValue2JsonVar(ConfigFile,"temperature","Tman")
			else:
				TemperatureSetPoint = SearchValue2JsonVar(ConfigFile,"temperature","Tice")	# Metto la piu` bassa (se non e` stata mal configurata)
			# Calcola Temperatura Termostato
			SensoreTermostato = SearchValue2JsonVar(ConfigFile,"pid","termostato")
			# adesso lo vado a cercare .. lui ed il valore ..
			# prima la directory
			Dir1w = SearchValueJsonVar(ConfigFile,"dir1w")
			# il file di lettura e` fisso ? forse meglio inserire anche questo nel file conf.json
			EndFilename = SearchValueJsonVar(ConfigFile,"file1w")
			Sensori = SearchValueJsonVar(ConfigFile,"sensori")
			for i in range(len(Sensori)):
				if Sensori[i]["name"] == SensoreTermostato:
					Sensore = open(Dir1w+Sensori[i]["value"]+"/"+EndFilename,"r")
					# Controlla se gli ultimi caratteri della stringa letta sono uguali a
					if (Sensore.readline()[-4:-1]) == "YES":
						# Effettuo il calcolo della temperatura indicando che il valore e` intero
						# prima del calcolo e che e` una stringa per passarla in scrittura
						# Mi serve il valore per il confronto ed il comando dell'uscita
						TemperaturaLetta=int(Sensore.readline()[-6:-1])/1000
					else:
						TemperaturaLetta=TemperatureSetPoint	# Mi serve comunque un valore per andare avanti.
			print(TemperaturaLetta)
			# Devo tenere l'uscita spenta se sono in off (anche se ho impostato la Tice)
			# Poi forse e` meglio togliere, anche se ho dimenticato spento, non voglio
			# si ghiaccino le tubature ..
			if EnableCycle == "off":
				print("Spegni uscita",UscitaTermostato)
				GPIO.output(UscitaTermostato, False)
			else:
				# Prima della verifica si dovrebbe aggiungere la tolleranza/approssimazione
				# Leggo il valore
				# Temperatura inerziale in riscaldamento
				TemperaturaInerzialePositiva = int(SearchValue2JsonVar(ConfigFile,"pid","tempcycle+"))/10	# Decimi di grado
				# Temperature inerziale in "raffreddamento"
				TemperaturaInerzialeNegativa = int(SearchValue2JsonVar(ConfigFile,"pid","tempcycle-"))/10	# Decimi di grado
				# Se temperatura set point meno temperatura d'inerzia e` minore della lettura
				if TemperaturaLetta + TemperaturaInerzialePositiva > int(TemperatureSetPoint):
					print("Accendi uscita",UscitaTermostato)
					GPIO.output(UscitaTermostato, True)
				# Se set point - inerziale e` maggiore
				elif TemperaturaLetta + TemperaturaInerzialePositiva < int(TemperatureSetPoint):
					print("Spegni uscita",UscitaTermostato)
					GPIO.output(UscitaTermostato, False)
				#if abs(int(TemperatureSetPoint) - TemperaturaLetta) > TemperaturaApprossimazione:
				#	if int(TemperatureSetPoint) > TemperaturaLetta:
				#		print("Accendi uscita",UscitaTermostato)
				#		GPIO.output(UscitaTermostato, True)
				#	else:
				#		print("Spegni uscita",UscitaTermostato)
				#		GPIO.output(UscitaTermostato, False)
				#################################################################################
			# Devo azzerare tempi e rileggere le variabili ..
			TempoInizio[1] = int(time.time())
			ConfigFile = ReadJsonFile("config.json")
			# Devo calcolare i tempi ciclo
			# Grafico
			TempoGrafico = int(SearchValue2JsonVar(ConfigFile,"graph","minutegraph"))*60	# trasformo in secondi
			# Ciclo
			TempoCiclo = int(SearchValue2JsonVar(ConfigFile,"pid","minutecycle"))*60	# trasformo in secondi
		
except KeyboardInterrupt:
	GPIO.cleanup()
