"""

Script à lancer en premier

"""
import subprocess

def run_script(script):
    proc = subprocess.Popen(['bash', '-c', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode:
        raise print("Erreur script: " + stderr)
    return stdout

retour = run_script('./script_bash')
print(retour)