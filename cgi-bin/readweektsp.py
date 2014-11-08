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


# Mi servono i files di configurazione, se esistono li apro, se no setto un'errore
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

if os.path.exists("weektsp.json"):
	try:
		with open("weektsp.json") as JsonFileWtsp:
			WtspFile = json.load(JsonFileWtsp)
			JsonFileWtsp.close()
	except IOError:
		Error = "Errore di I/O \"weektsp.json\""
	except ValueError:
		Error = "Errore dati \"weektsp.json\", ritento .."
		time.sleep(5)
		with open("weektsp.json") as JsonFileWtsp:
			WtspFile = json.load(JsonFileWtsp)
			JsonFileWtsp.close()
	else:
		Error = ""
else:
	Error = "Errore, non trovo il file \"weektsp.json\""


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
<h2>Configurazione temperature giornaliero/settimanali</h2>
<br/>
<br/>
""")


print("<p><hr/></p><br/>")	# Stampa un linea orizzontale

# Cerco ..
for i in range(len(ConfigFile)):
	if "temperature" == (ConfigFile[i]["name"]):
		# Appoggio a variabile l'array
		TempsArray = ConfigFile[i]["value"]


# Start FORM input
# write*.py
print("<form action=\"/cgi-bin/writeweektsp.py\" method=\"post\">")
print("<table>")

for j in range(len(WtspFile)):
	print("<tr><td>Ora:</td>\
	<td>00</td><td>01</td><td>02</td><td>03</td><td>04</td><td>05</td>\
	<td>06</td><td>07</td><td>08</td><td>09</td><td>10</td><td>11</td>\
	<td>12</td><td>13</td><td>14</td><td>15</td><td>16</td><td>17</td>\
	<td>18</td><td>19</td><td>20</td><td>21</td><td>22</td><td>23</td>\
	</tr>")
	# per tutta la lunghezza delle temperature (3)
	for i in range(len(TempsArray)):
		if "Tman" != TempsArray[i]["name"]:	# Esclude la temperatura manuale
			print("<tr><td>",TempsArray[i]["display"],": </td>")
			# Per tutta la lunghezza/voci contenute nell'array .. ore
			for k in range(len(WtspFile[j]["hours"])):
				# Se la temperatura oraria corrisponde ad un setpoin, marco il settaggio
				#print (WtspFile[j]["hours"][k]["temperature"], "||", TempsArray[i]["name"],"<br>")
				if WtspFile[j]["hours"][k]["temperature"] == TempsArray[i]["name"]:
					Checked="checked"
				else:
					Checked=""
				# Concatenamento 
				print("<td><input type=\"radio\" name=\"",WtspFile[j]["day"],k,"\" value=\"",TempsArray[i]["name"],"\" ",Checked,"> </td>", sep="")
	print("</tr>")
	print("<tr><td><b>",WtspFile[j]["day"],"</b></td><td colspan=\"24\"><hr></td></tr>")

print("<tr>")
print("<td></td><td colspan=\"24\"><input type=\"submit\" value=\"Submit\"></td>")
print("</tr>")
print("</table>")
print("</form>")	# END form


# End body/End html
print("""
</body>
</html>
""")
