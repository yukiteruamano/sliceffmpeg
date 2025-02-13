import subprocess
import argparse
import logging

def parse_time(time_str):
    """
    Convierte un timestamp en formato HH:MM:SS a segundos.

    Args:
        time_str (str): El timestamp en formato HH:MM:SS.

    Returns:
        int: El tiempo en segundos.
    """
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s


def generate_ffmpeg_command(input_video, time_init, time_final, output_video):
    """
    Genera el comando ffmpeg para cortar el video.

    Args:
        input_video (str): Ruta completa del archivo de video de entrada.
        time_init (int): Tiempo de inicio en segundos.
        time_final (int): Tiempo de finalización en segundos.
        output_video (str): Ruta completa del archivo de video de salida.

    Returns:
        list: Lista de argumentos para el comando ffmpeg.
    """
    return [
        'ffmpeg', '-i', input_video, '-map', '0', '-c', 'copy',
        '-ss', str(time_init), '-t', str(time_final - time_init),
        '-map_metadata', '0', output_video
    ]


def setup_logging():
    """
    Configura el logging para escribir en un archivo y en la consola.
    """
    logging.basicConfig(
        filename='cut_video.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


def main():
    """
    Función principal que procesa el video según los timestamps en un archivo slice.txt.
    """
    parser = argparse.ArgumentParser(description='Cortar un video según timestamps en un archivo slice.txt.')
    parser.add_argument('-i', required=True, help='Ruta completa del archivo de video de entrada.')
    parser.add_argument('-slice', required=True, help='Ruta completa del archivo slice.txt.')

    args = parser.parse_args()

    input_video = args.i
    slice_file = args.slice

    setup_logging()
    logging.info(f"Iniciando procesamiento del video: {input_video}")
    logging.info(f"Usando archivo slice: {slice_file}")

    try:
        with open(slice_file, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        logging.error(f"El archivo slice.txt no se encontró en la ruta especificada: {slice_file}")
        return
    except Exception as e:
        logging.error(f"Error al leer el archivo slice.txt: {e}")
        return

    for i, line in enumerate(lines):
        try:
            start_time, end_time = line.strip().split()
            time_init = parse_time(start_time)
            time_final = parse_time(end_time)
            output_video = f"{input_video.split('.')[0]}-{str(i + 1).zfill(3)}.mp4"

            logging.info(f"Procesando línea {i + 1}: {line.strip()}")
            logging.info(f"Transformando tiempos: {start_time} -> {time_init} segundos, {end_time} -> {time_final} segundos")

            command = generate_ffmpeg_command(input_video, time_init, time_final, output_video)
            logging.info(f"Ejecutando: {' '.join(command)}")
            subprocess.run(command, check=True)
            logging.info(f"Video cortado y guardado como: {output_video}")
        except ValueError as ve:
            logging.error(f"Error al procesar la línea {i + 1}: {ve}")
        except subprocess.CalledProcessError as cpe:
            logging.error(f"Error al ejecutar ffmpeg para la línea {i + 1}: {cpe}")
        except Exception as e:
            logging.error(f"Error inesperado en la línea {i + 1}: {e}")

    logging.info("Proceso completado.")


if __name__ == "__main__":
    main()