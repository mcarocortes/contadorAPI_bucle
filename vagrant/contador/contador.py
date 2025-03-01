import random
import time
import pyodbc
import socket
import fcntl
import struct

def get_ip(ifname):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15].encode('utf-8'))
            )[20:24])
    except IOError:
        print("No se pudo obtener la IP de la interfaz:")
        return "0.0.0.0"


# Función para generar datos simulados
def generate_data():
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')  # Formato de fecha y hora para SQL Server
    medida = random.uniform(10.0, 100.0)  # Genera un número decimal aleatorio entre 10 y 100
    interface = 'enp0s8'
    ip = get_ip(interface)  # Obtiene la dirección IP de la máquina virtual
    return ip, timestamp, medida

# Conexión a la base de datos SQL Server
def send_data_to_db(ip, timestamp, medida):
    try:
        # Configurar la conexión
        connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=192.168.0.10\\SQLEXPRESS;"  # Nombre del servidor y instancia
            "DATABASE=contadores;"  # Nombre de la base de datos
            "UID=usr_cont;"  # Nombre de usuario
            "PWD=pass123;"  # Contraseña
            "Encrypt=no;"  # Deshabilita el cifrado SSL
        )

        # Establece la conexión
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Inserta los datos en la tabla
        query = "INSERT INTO pulsos (ip, tiempo, medida) VALUES (?, CONVERT(datetime, ?, 120), ?)"
        cursor.execute(query, (ip, timestamp, medida))
        connection.commit()

        print("Datos enviados: ip={}, tiempo={}, medida={}".format(ip, timestamp, medida))  # Formato tradicional

    except Exception as e:
        print("Error al enviar datos: {}".format(e))  # Formato tradicional
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    ip, timestamp, medida = generate_data()
    send_data_to_db(ip, timestamp, medida)