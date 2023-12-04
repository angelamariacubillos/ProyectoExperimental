import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import os

archivo_dat = "datosoctubre.txt"

mes = archivo_dat[5:]
mes = mes[:-4]
df = pd.read_csv(archivo_dat, sep=';', skiprows=42, header=None)
horaUTC = df[0]
T = df[2]
V = df[3]
brillo = df[4]

horas_utc = [datetime.strptime(hora, '%Y-%m-%dT%H:%M:%S.%f') for hora in horaUTC]
horas_bogota = [hora - timedelta(hours=5) for hora in horas_utc]
horas_nocturnas = [hora for hora in horas_bogota if hora.hour >= 17 or hora.hour <= 7]
horas_nocturnas.sort()
noches_separadas = []
noche_actual = []

for hora in horas_nocturnas:
    if not noche_actual:
        noche_actual.append(hora)
    elif (hora - noche_actual[-1]).seconds > 6 * 3600:
        noches_separadas.append(noche_actual)
        noche_actual = [hora]
    else:
        noche_actual.append(hora)

noches_separadas.append(noche_actual)

for idx, noche in enumerate(noches_separadas):
    plt.figure(figsize=(10, 6))

    brillo_noche = [brillo[horas_bogota.index(hora)] for hora in noche]

    plt.ylabel(r'$\mathbf{Brillo\ (mag/arcsec^2)}$', weight='bold')
    plt.title('Diagrama de Caja y Bigotes', weight='bold', fontsize=20, y=1.06)

    fecha_noche = noche[idx].strftime('%d-%m-%Y')
    dia = fecha_noche[:2]
    plt.suptitle(f'{fecha_noche}', weight='bold', fontsize=14, y=0.92)

    plt.boxplot(brillo_noche, vert=True, medianprops={'color': 'blue'})
    
    plt.grid(True)
    
    media = np.mean(brillo_noche)
    desviacion_estandar = np.std(brillo_noche)
    
    plt.text(0.75, 0.9, f'Media: {media:.2f}', transform=plt.gca().transAxes)
    plt.text(0.75, 0.85, f'Desviación Estándar: {desviacion_estandar:.2f}', transform=plt.gca().transAxes)
    
    carpeta_destino = "C:/Users/angel/Documents/SEMESTRE 7/Proyecto Experimental/GRAFICAS/Caja y Bigotes/" + mes.upper()
    nombre_archivo = carpeta_destino + "/" + dia + mes + "2023.png"
    
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
    nombre_archivo = carpeta_destino + "/" + dia + mes + "2023.png"
    plt.savefig(nombre_archivo)
    
plt.show()
