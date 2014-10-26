#!/usr/bin/env python3

import os

import json

import cgi
import cgitb

cgitb.enable()

# Mi serve il file dei setpoins
# Se il file esiste lo apro, se no, genero entrambi SetPoints e file
if os.path.exists("setpointarray.json"):
	with open("setpointarray.json") as JsonFileSetPoints:
		SetPoints = json.load(JsonFileSetPoints)
else:
	# Qua si dovrebbe mettere un'errore e fermare l'esecuzione
	# invece di generarlo
	SetPoints = \
		[	\
		    { "display": "Temperatura Giorno", "name": "Tday", "temperature": "20" },	\
		    { "display": "Temperatura Notte", "name": "Tnight", "temperature": "16" },	\
		    { "display": "Temperatura Antigelo", "name": "Tice", "temperature": "5" },	\
		]
	
	with open("setpointarray.json", "w") as OutfileSetPoints:
		json.dump(SetPoints, OutfileSetPoints, indent=4)

# Questo e` il file di setpoint giornaliero
# Se il file esiste lo apro, se no, genero entrambi SetPoints e file
if os.path.exists("dayssetpointarray.json"):
	with open("dayssetpointarray.json") as JsonFileDays:
		DaysSetPoints = json.load(JsonFileDays)
else:
	DaysSetPoints = ""
	
	with open("dayssetpointarray.json", "w") as outfile:
		json.dump(DaysSetPoints, outfile, indent=4)


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

print("""
<h2>Configurazione temperature giornaliere</h2>
<p><b>ATTENZIONE</b>: ???</p>
<p>???</p>
<br/>
<br/>
""")

# Start form input
print("<form action=\"/cgi-bin/writedayssetpoints.py\" method=\"post\">")
print("<table>")

# Per tutta la lunghezza/voci contenute nell'array .. giorni
for j in range(len(DaysSetPoints)):
	print("<tr><td>Ora:</td>\
	<td>00</td><td>01</td><td>02</td><td>03</td><td>04</td><td>05</td>\
	<td>06</td><td>07</td><td>08</td><td>09</td><td>10</td><td>11</td>\
	<td>12</td><td>13</td><td>14</td><td>15</td><td>16</td><td>17</td>\
	<td>18</td><td>19</td><td>20</td><td>21</td><td>22</td><td>23</td>\
	</tr>")
	# per tutta la lunghezza delle temperature (3)
	for i in range(len(SetPoints)):
		print("<tr><td>",SetPoints[i]["display"],": </td>")
		# Per tutta la lunghezza/voci contenute nell'array .. ore
		for k in range(len(DaysSetPoints[j]["hours"])):
			# Se la temperatura oraria corrisponde ad un setpoin, marco il settaggio
			#print (DaysSetPoints[j]["hours"][k]["temperature"], "||", SetPoints[i]["name"],"<br>")
			if DaysSetPoints[j]["hours"][k]["temperature"] == SetPoints[i]["name"]:
				Checked="checked"
			else:
				Checked=""
			# Concatenamento 
			print("<td><input type=\"radio\" name=\"",DaysSetPoints[j]["day"],k,"\" value=\"",SetPoints[i]["name"],"\" ",Checked,"> </td>", sep="")
	print("</tr>")
	print("<tr><td>")
	print("<b>",DaysSetPoints[j]["day"],"</b><hr></br>")
	print("<td></tr>")


print("<td><input type=\"submit\" value=\"Submit\"></td>")
print("</table>")
print("</form>")	# END form


# End body/End html
print("""
</body>
</html>
""")
