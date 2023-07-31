import pandas as pd
import json
from urllib.request import urlopen
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
import locale
import numpy as np
import seaborn as sns

locale.setlocale(locale.LC_ALL, 'es_ES')

DIA = 'dia'
ESTACION = 'estaci'
NIVEL = 'nivell_absolut'
PORCENTAJE_EMBALSADO = 'percentatge_volum_embassat'
VOLUMEN_EMBALSADO = 'volum_embassat'

"""
URL con los datos de los embalses
cada registro contiene
  dia: fecha de la medición
  estaci: nombre del embalse
  nivell_absolut: máxima altura sobre el nivel del mar del embalse
  percentatge_volum_embassat: porcentaje del volumen de agua embalsada
  volum_embassat: volumen de agua embalsada en hectómetros cúbicos
"""
url = "https://analisi.transparenciacatalunya.cat/resource/gn9e-3qhr.json"

# se abre el recurso, se cargan los datos y se normalizan en un Dataframe
response = urlopen(url)
data = json.loads(response.read())
df = pd.json_normalize(data)

# total de filas y columnas, y contadores para distribuir los gráficos
fila = 0
columna = 0
totalFilas = 3
totalColumnas = 3

# crear objetos de fecha a partir de la columna 'dia'
df[DIA] = pd.to_datetime(df[DIA])

# convertir a float los valores de porcentaje de agua embalsada
df[PORCENTAJE_EMBALSADO] = df[PORCENTAJE_EMBALSADO].apply(lambda x: float(x))

# # obtener la lista de los embalses
# embalses = df[ESTACION].unique().tolist()

# # generar la figura y la lista de gráficos
# fig, axs = plt.subplots(nrows= totalFilas, ncols= totalColumnas)

# # estilo y título de la figura
# fig.set_facecolor('papayawhip')
# fig.set_edgecolor('orange')
# fig.set_linewidth(2)
# fig.suptitle('Estado de los embalses (% agua embalsada)', fontsize = 14)

# for e in embalses:
#   #título del gráfico, separando por líneas, si se puede, embalse y población
#   titulo = e
#   separacion = e.find('(')

#   if (separacion > -1):
#     titulo = e[0: separacion - 1] + "\n" + e[separacion:]
  
#   # obtener los datos de los últimos diez días para un embalse
#   df10dias = df[df[ESTACION] == e].head(10)

#   # para crear las marcas del eje de las fechas con los días
#   locator = mdates.DayLocator()

#   # formateo de las marcas del eje de las fechas
#   formatter = mdates.ConciseDateFormatter(locator)

#   # asignación de marcas, formato y etiqueta del eje de las fechas
#   axs[fila, columna].xaxis.set_major_locator(locator)
#   axs[fila, columna].xaxis.set_major_formatter(formatter)
#   axs[fila, columna].set_xlabel('Fechas')

#   # se establecen los límites y la etiqueta para el eje y
#   minimo = df10dias[PORCENTAJE_EMBALSADO].min()
#   maximo = df10dias[PORCENTAJE_EMBALSADO].max()
#   axs[fila, columna].set_ylim(minimo - 0.1, maximo + 0.1)
#   axs[fila, columna].set_ylabel('%')

#   # titulo y estilo para la rejilla de gráfico
#   axs[fila, columna].set_title(titulo, fontsize = 10)
#   axs[fila, columna].grid(linestyle = '-.', linewidth = 0.5, color = '.25')

#   # dibujar los datos
#   axs[fila, columna].plot(df10dias[DIA], df10dias[PORCENTAJE_EMBALSADO], marker="o", linestyle="dashed")

#   # actulizar la columna y fila para acceder al siguiente gráfico
#   columna = columna + 1
#   if (columna == 3):
#     columna = 0
#     fila = fila + 1
  
# # establecer la etiqueta de la figura y mostrarla con los gráficos
# fig.set_label('Agua embalsamada (%)')
# plt.tight_layout()
# plt.show()
# # plt.savefig('grafico.png')

#gráficos de barras con % por embalse

datosBarras = df.head(9)
embalses = list(datosBarras[ESTACION].to_numpy())
for index in range(len(embalses)):
  e = embalses[index]
  titulo = e
  separacion = e.find('(')

  if (separacion > -1):
    titulo = e[0: separacion - 1] + "\n" + e[separacion:]

  embalses[index] = titulo

#con Matplotlib

figBarras, axBarras = plt.subplots()

y = list(datosBarras[PORCENTAJE_EMBALSADO].to_numpy(dtype=float))
x = embalses

axBarras.barh(x, y)
axBarras.set_xlim(0, 100)
axBarras.set_xlabel('% agua embalsada')

figBarras.tight_layout()

plt.show()

# con Seaborn

sns.set_theme(style = "whitegrid")
sns.set_color_codes("pastel")

figBarrasSB, axBarrasSB = plt.subplots()

sns.barplot(
  x = list(datosBarras[PORCENTAJE_EMBALSADO].to_numpy(dtype=float)),
  y = embalses,
  orient = "h",
)

axBarrasSB.set(xlim=(0, 100), xlabel = '% agua embalsada')

sns.despine(left = True, bottom = True)

figBarrasSB.tight_layout()

plt.show()
