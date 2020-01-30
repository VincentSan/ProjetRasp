"""

Script à lancer en premier

"""
import subprocess
import mysql.connector
from httplib2 import Http
from json import dumps

#Lancer des scripts bash et recuperer leur résultat
def run_script(script):
    #Lance le programme
    proc = subprocess.Popen(['bash', '-c', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    #Voir s'il y a des erreurs
    if proc.returncode:
        raise print("Erreur script: " + stderr)
    #Envoie le resultat
    return stdout

#Pour envoyer des messages au chat discord
def message(jsonFile):
    #URL Webhooks
    url = 'URL-NAME'
    bot_message = jsonFile

    message_headers = { 'Content-Type': 'application/json; charset=UTF-8'}

    http_obj = Http()

    http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )

retour = run_script('./script_bash')

#Recuperer la Date + Heure.
date = retour[2:19]
temp = retour[25:29]

#Prepare la requete insertion
inser = (date, temp)

conn = mysql.connector.connect(host="localhost",user="admin",password="azerty", database="grafana_metrics")
cursor = conn.cursor()
cursor.execute(""" INSERT INTO `TEMPERATURE_CPU_CP` (`CP_TIME`, `CP_TEMP`) VALUES (%s, %s) """, inser)
conn.commit() #Commit les modification
conn.close() #Ferme la base

#Si on doit lever une alert
if float(temp) > 79.0:
    #JsonMessage est de type dict
    jsonMessage = {
                    "embeds": [
                        {
                        "footer": {
                        "text": "{0}".format(date),
                        "icon_url": "https://vignette.wikia.nocookie.net/spiderriders/images/d/dd/Discord.png/revision/latest?cb=20171218232913"},
                        "thumbnail": {
                        "url": "http://ec.europa.eu/eurostat/cache/infographs/youthday2016/img/embed.png"},
                        "title": "[ALERT] Problème avec le RasberryPI 3",
                        "description": "Température actuel : {0}°C.\n\n\n[🚀 GRAFANA \n](http://framboise:3000)\n".format(temp),
                        "color": 16711680
                    }
                    ]
                }
    message(jsonMessage)