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
<h2>Configurazione uscite</h2>
<p>Sono quelle della GPIO utilizzate dal Raspberry Pi</p>
<p><b>ATTENZIONE</b>: Verificare il tipo di Raspberry Pi in uso</p>
<p>La presente selezione e` (dovrebbe) standardizzata per il tipo "B" (no "A" e no "B+")</p>
<p>Ho previsto i soli valori dei GPIO "liberi" (che non hanno altre funzioni)</p>
<p>Al momento ho messo e usato i valori della GPIO, poi valuteremo se meglio segnare il pin.
Anche un'altra cosa, quella "ricorsione" per la ricerca dell'errore, da vedere se si riesce
a farla piu` pulita, e` che non volevo usare una funzione, ma forse per questo caso e`
meglio.</p>
<br/>
<br/>
""")

print("<p><hr/></p><br/>")	# Stampa un linea orizzontale


# Start FORM input
# writesensors.py
print("<form action=\"/cgi-bin/writeoutgpio.py\" method=\"post\">")
#print("<table>")

print("<p></p>")
print("Seleziona l'uscita Termostato: ")
# Cerco il "gpio" nel file config.json
for i in range(len(ConfigFile)):
	if "outgpio" == (ConfigFile[i]["name"]):
		# Cerco i valori dei pin della gpio
		for j in range(len(ConfigFile)):
			if "outfreegpio" == (ConfigFile[j]["name"]):
				# Inizo ad "impostare" la form
				print("<select name=\"outgpio\">")
				for k in (ConfigFile[j]["value"]).split(","):	# .split() converte una stringa in lista, fra parentesi il separatore (la virgola)
					# Controllo il valore preimpostato e setto/resetto la selezione
					if k == ConfigFile[i]["value"]:
						Selected="selected"
					else:
						Selected=""
					print("<option value=\"",k,"\"",Selected,">",k,"</option>", sep="")
				print("</select>")

print("<p></p>")
print("Seleziona l'uscita di accensione/abilitazione riscaldamento: ")
# Cerco il "enable" nel file config.json
for i in range(len(ConfigFile)):
	if "enable" == (ConfigFile[i]["name"]):
		# Cerco i valori dei pin della gpio
		for j in range(len(ConfigFile)):
			if "outfreegpio" == (ConfigFile[j]["name"]):
				# Inizo ad "impostare" la form
				print("<select name=\"enable\">")
				for k in (ConfigFile[j]["value"]).split(","):	# .split() converte una stringa in lista, fra parentesi il separatore (la virgola)
					# Controllo il valore preimpostato e setto/resetto la selezione
					if k == ConfigFile[i]["value"]:
						Selected="selected"
					else:
						Selected=""
					print("<option value=\"",k,"\"",Selected,">",k,"</option>", sep="")
				print("</select>")

print("<p></p>")
print("Seleziona l'uscita di accensione impianto: ")
# Cerco il "plant" nel file config.json
for i in range(len(ConfigFile)):
	if "plant" == (ConfigFile[i]["name"]):
		# Cerco i valori dei pin della gpio
		for j in range(len(ConfigFile)):
			if "outfreegpio" == (ConfigFile[j]["name"]):
				# Inizo ad "impostare" la form
				print("<select name=\"plant\">")
				for k in (ConfigFile[j]["value"]).split(","):	# .split() converte una stringa in lista, fra parentesi il separatore (la virgola)
					# Controllo il valore preimpostato e setto/resetto la selezione
					if k == ConfigFile[i]["value"]:
						Selected="selected"
					else:
						Selected=""
					print("<option value=\"",k,"\"",Selected,">",k,"</option>", sep="")
				print("</select>")

print("<p></p>")
print("<input type=\"submit\" value=\"Submit\"></td>")
#print("</table>")
print("</form>")	# END form


# End body/End html
print("""
</body>
</html>
""")
