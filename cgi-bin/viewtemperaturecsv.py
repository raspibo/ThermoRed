#!/usr/bin/env python3

# Copia files nel .bak

#import csv
#import os

# Serve per la parte di gestione html in python
import cgi
import cgitb

import time
# Abilita gli errori al server web/http
cgitb.enable()


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


FileTemp = open("temperature.csv","r")
FileCSV = FileTemp.read()
FileTemp.close()
print("La visualizzazione non e` il massimo, ma tanto per rendere l'idea.<br/><br/>")
print("<b>Contenuto del file \"temperature.csv\":</b><br/><br/>")

for i in FileCSV:
	print(i)
	if i == "\n":
		print("<br/>")
#print(FileCSV)

"""
if os.path.exists("temperature.csv"):
	try:
		with open("temperature.csv") as csvfile:
			TempFileCSV = cvs.reader(cvsfile, delimiter=",", quotechar="|")
			cvsfile.close()
	except IOError:
		Error = "Errore di I/O \"temperature.csv\""
	except ValueError:
		Error = "Errore dati \"temperature.csv\", ritento .."
		time.sleep(5)
		with open("temperature.csv") as csvfile:
			TempFileCSV = cvs.reader(cvsfile, delimiter=",", quotechar="|")
			cvsfile.close()
	else:
		Error = ""
else:
	Error = "Errore, non trovo il file \"temperature.csv\""

if Error != "":
	print("<h1>",Error,"</h1><br/>")

for row in TempFileCSV:
	print(",".join(row),"<br/>")
"""

# End body/End html
print("""
</body>
</html>
""")
