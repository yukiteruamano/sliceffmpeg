# Sliceffmpeg - Utilidad para cortar videos en ffmpeg

`Sliceffmpeg` es una herramienta de línea de comandos diseñada para facilitar el proceso de corte de videos utilizando `ffmpeg`. Esta herramienta permite a los usuarios especificar el tiempo de inicio y el tiempo de fin del corte, y luego genera el comando `ffmpeg` correspondiente para realizar el corte. El formato del archivo slice.txt es el siguiente: 

`time_init time_end`

 Donde los timestamp deben estar descritos formato: `00:00:00 (horas:minutos:segundos)` 
 
 Así nos quedaría:
 
`00:00:00 00:00:10` (Primeros 10 segundos del vídeo)

`00:00:10 00:00:20` (Del segundo 10 al 20)

`00:00:20 00:00:30` (Del segundo 20 al 30)
  
Y así sucesivamente, cada línea del archivo `slice.txt` representa un intervalo de tiempo que se desea cortar del video.

## Información para desarrollo

El script está desarrollado usando python, ruff y uv, instala las herramientas y disfruta. 