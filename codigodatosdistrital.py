import pandas as pd
from datetime import datetime, timedelta


archivo_dat = "datosdistrital.csv"

df = pd.read_csv(archivo_dat, sep=',', skiprows=6, header=None,encoding='utf-8', parse_dates=[0], dayfirst=True)
fecha = df[0]
P = df[1]
T = df[2]
H = df[3]



print(fecha[2805].second)