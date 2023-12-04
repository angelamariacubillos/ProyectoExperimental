import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import pandas as pd
import os

archivo_dat="datosoctubre.txt" 

mes=archivo_dat[5:]
mes=mes[:-4]
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
    
    fig, ax1 = plt.subplots(figsize=(10, 6))

    brillo_noche = [brillo[horas_bogota.index(hora)] for hora in noche]
    T_fi = [T[horas_bogota.index(tem)] for tem in noche]
    

    ax1.plot(noche, brillo_noche, color='teal', label="Brillo")
    ax1.set_xlabel('Hora Local (Bogotá)', weight='bold')
    ax1.set_ylabel(r'$\mathbf{Brillo\ (mag/arcsec^2)}$', weight='bold')
    ax1.invert_yaxis()

    ax2 = ax1.twinx()
    ax2.plot(noche, T_fi, color='r', label="T")
    ax2.set_ylabel(r'$\mathbf{Temperatura\ (°C)}$', weight='bold')

    formatoho = mdates.DateFormatter('%H:%M')
    ax1.xaxis.set_major_formatter(formatoho)

    plt.title('Brillo y Temperatura', weight='bold', fontsize=20, y=1.06)
    
    fecha_noche = noche[idx].strftime('%d-%m-%Y')
    dia=fecha_noche[:2]
    plt.suptitle(f'{fecha_noche}', weight='bold', fontsize=14, y=0.87)
    
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="lower left")
    #ax1.legend(lines1 + lines2, labels1 + labels2, bbox_to_anchor=(0.6, 1), bbox_transform=ax1.transAxes)
    
    
    ax1.grid(True, axis='x', linestyle='-', alpha=0.7)
    ax1.grid(True, axis='y', linestyle='-.', alpha=0.7)
    ax2.grid(True, axis='y', linestyle='-', alpha=0.7)
             
    plt.tight_layout()
    carpeta_destino="C:/Users/angel/Documents/SEMESTRE 7/Proyecto Experimental/GRAFICAS/Brillo y Temperatura/"+mes.upper()
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
    nombre_archivo=carpeta_destino+"/"+dia+mes+"2023.png"
    plt.savefig(nombre_archivo)