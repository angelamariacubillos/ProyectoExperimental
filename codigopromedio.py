import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib.ticker import FuncFormatter
import pandas as pd
import numpy as np

archivo_dat="datosagosto.txt" 

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

nocturnas_final =[]

hf = [hora.strftime('%H:%M') for hora in horas_bogota]

minutos_bogota = []

for hora in horas_bogota:
    
    ange = 0
    
    if hora.hour <= 7:
        
        ange = 24
        
    else:
        
        ange = 0
        
    minutos_bogota.append((hora.hour+ange) * 60 + hora.minute)
    

plt.figure(figsize=(9.5, 6))

noche_sumadas = np.zeros(180)
inter = np.linspace(1020,1920,180)
cantidad =np.zeros(180)

for idx, noche in enumerate(noches_separadas):
    
    brillo_noche = [brillo[horas_bogota.index(hora)] for hora in noche]
    
    juan = [minutos_bogota[horas_bogota.index(hora)] for hora in noche]

    plt.plot(juan, brillo_noche, color='skyblue', linewidth = 1)
    
    
    for idx, p in enumerate(juan):
        peras = (p-1020)//5
        noche_sumadas[peras] += brillo_noche[idx]
        cantidad[peras] +=1
    
noche_promedio = noche_sumadas/cantidad
    
plt.plot(inter,noche_promedio, color="navy", label ="Brillo Promedio")    
plt.gca().invert_yaxis()


plt.xlabel('Hora Local (Bogotá)', weight='bold') 
plt.ylabel(r'$\mathbf{Brillo\ (mag/arcsec^2)}$', weight='bold') 

plt.title('Brillo General Octubre', weight='bold', fontsize=25, y=1.06)
plt.suptitle('Brillo Promedio', weight='bold', fontsize=14, y=0.85)

def nombre(m,c):
    
    ho = m//60
    guayaba = m%60
    
    if m > 1440:
        m = m - 1440
        ho = m//60

    if ho < 10:
        ho = "0"+str(ho)
        
    if guayaba < 10:
        guayaba = "0"+str(guayaba)   
    
    ho=str(ho)
    ho=ho[:2]
        
    guayaba=str(guayaba)
    guayaba=guayaba[:2]

    return (ho+":"+guayaba)

formatter = FuncFormatter(nombre)
plt.gca().xaxis.set_major_formatter(formatter)

plt.legend(loc="upper left")

plt.tight_layout()

    


