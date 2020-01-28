"""

Script à lancer en premier

"""
import subprocess
import mysql.connector

def run_script(script):
    proc = subprocess.Popen(['bash', '-c', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode:
        raise print("Erreur script: " + stderr)
    return stdout

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
if temp > 79:
    run_script('./alert_bash ' + date + " " + temp)