#!/usr/bin/env python3

## Note
# Ho inserito alcune annotazioni all'interno del programma.
# Riassumendo il discorso multi-sensore, forse e` bene realizzare
# qualcosa di differente ? Ma cosa ? E come ?

import time

# Lettura file sonda temperatura
# ATTENZIONE: il file temperatura e` differente per ogni sensore !!!!
# Qua e` da pensare una possibile variante o cosa/come
# Ci ho pensato su, sarebbe coumnque una cosa da verificare,
# Perche` non e` detto che la sonda 1 sia in bagno, piuttosto che in
# camera, la 2 potrebbe essere nel salotto ..
# Quindi non so se e quanto ne vale la pena. Oggi!
FileSondaT = open('/sys/bus/w1/devices/10-0008029444b6/w1_slave','r')

# Devo aggiungere il file dei setpoin temperature
#FileSetPoint = open('setpointtemperature','r')

# Anche questo file, la riga di intestazione sara` "in dipendenza di",
# quindi un'altra cosa da valutare.
# Apertura file temperature.csv in "append mode"
FileTempsCSV = open('temperature.csv','a')

## Devo scrivere il file CSV con i parametri separati da virgole
## La struttura che ho pensato di utilizzare e`:
## Data,Temperatura di Setpoint, Temperatura 1
# Quindi per primo, scrivo la data+ora nel file
FileTempsCSV.write(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))
# Aggiungo la virgola di separazione
FileTempsCSV.write(',')
# Prima devo "calcolare" il setpoint
# Metto un valore a caso
SetPoint = '25'
# Poi scrivo il setpoit richiesto
FileTempsCSV.write(SetPoint)
# Aggiungo la virgola di separazione
FileTempsCSV.write(',')

## Qua si dovrebbe aggiungere un ciclo "for", per ogni sonda di
## temperatura da inserie nel grafico, per adesso e` una, quindi
## semplifichiamo.
# Controlla se gli ultimi caratteri della stringa letta sono uguali a
if (FileSondaT.readline()[-4:-1]) == "YES":
    # Effettuo il calcolo della temperatura indicando che il valore e` intero
    # prima del calcolo e che e` una stringa per passarla in scrittura
    FileTempsCSV.write(str(int(FileSondaT.readline()[-6:-1])/1000))
else:
    FileTempsCSV.write('err')	# err, se errore sonda, non so ancora cosa fara` il grafico perche` non e` successo.

# Aggiungo il ritorno a capo di fine riga per i valori successivi
FileTempsCSV.write('\n')

FileSondaT.close()
FileTempsCSV.close()