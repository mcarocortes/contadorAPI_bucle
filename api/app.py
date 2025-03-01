from flask import Flask, jsonify, request
import pyodbc

app = Flask(__name__)

# Configuración de la conexión a SQL Server
def get_db_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=192.168.0.10\\SQLEXPRESS;"  
        "DATABASE=contadores;"  
        "UID=usr_cont;"  # Nombre de usuario
        "PWD=pass123;"  # Contraseña
    )
    return conn

# Ruta para obtener todos los datos de la tabla
@app.route('/api/pulsos', methods=['GET'])
def obtener_datos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pulsos")  # Reemplaza con tu tabla
        datos = cursor.fetchall()
        conn.close()

        # Convertir los datos a un formato JSON
        resultado = []
        for fila in datos:
            resultado.append({
                'id': fila[0],
                'ip': fila[1],
                'tiempo': fila[2],
                'medida': fila[3]
            })

        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para obtener datos por IP
@app.route('/api/pulsos/<ip>', methods=['GET'])
def obtener_datos_por_ip(ip):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pulsos WHERE ip = ?", ip)  # Reemplaza con tu tabla
        datos = cursor.fetchall()
        conn.close()

        # Convertir los datos a un formato JSON
        resultado = []
        for fila in datos:
            resultado.append({
                'id': fila[0],
                'ip': fila[1],
                'tiempo': fila[2],
                'medida': fila[3]
            })

        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Iniciar la aplicación Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)