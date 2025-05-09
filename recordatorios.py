import mysql.connector
import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta

# Configura tu conexión a la base de datos
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # tu contraseña de MySQL
    database="reservaciones_db"
)
cursor = conn.cursor()

# Configura tu cuenta de correo
REMITENTE = "pruebaprogramacion005@gmail.com"
CONTRASENA = "wxtkasvekthlnytg"

def enviar_recordatorio(destinatario, nombre, fecha_hora, numero_mesa):
    msg = EmailMessage()
    msg["Subject"] = "Recordatorio de tu reservación"
    msg["From"] = REMITENTE
    msg["To"] = destinatario
    msg.set_content(
        f"Hola {nombre},\n\n"
        f"Este es un recordatorio de tu reservación para mañana ({fecha_hora}).\n"
        f"Mesa asignada: {numero_mesa}.\n\n"
        f"¡Te esperamos!"
    )
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(REMITENTE, CONTRASENA)
            smtp.send_message(msg)
            print(f"Correo de recordatorio enviado a {destinatario}")
    except Exception as e:
        print(f"Error al enviar correo a {destinatario}: {e}")

def buscar_y_enviar_recordatorios():
    fecha_manana = (datetime.now() + timedelta(days=1)).date()

    cursor.execute("""
        SELECT nombre, email, fecha_hora, mesa_id FROM reservaciones 
        WHERE DATE(fecha_hora) = %s
    """, (fecha_manana,))
    reservaciones = cursor.fetchall()

    for nombre, email, fecha_hora, mesa_id in reservaciones:
        # Obtener el número de la mesa
        cursor.execute("SELECT numero FROM mesas WHERE id = %s", (mesa_id,))
        resultado = cursor.fetchone()
        numero_mesa = resultado[0] if resultado else "?"

        enviar_recordatorio(email, nombre, fecha_hora, numero_mesa)

buscar_y_enviar_recordatorios()
conn.close()
