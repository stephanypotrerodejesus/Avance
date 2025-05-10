import tkinter as tk
from tkinter import messagebox
import mysql.connector
import smtplib
from email.message import EmailMessage


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  
    database="reservaciones_db"
)
cursor = conn.cursor()


def reservar():
    nombre = entry_nombre.get()
    email = entry_email.get()
    fecha_hora = entry_fecha_hora.get()

    if not nombre or not email or not fecha_hora:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    try:
        
        cursor.execute("""
            SELECT id FROM mesas 
            WHERE id NOT IN (SELECT mesa_id FROM reservaciones WHERE fecha_hora = %s)
            LIMIT 1
        """, (fecha_hora,))
        mesa_disponible = cursor.fetchone()

        if mesa_disponible:
            mesa_id = mesa_disponible[0]
            cursor.execute("""
                INSERT INTO reservaciones (nombre, email, fecha_hora, mesa_id)
                VALUES (%s, %s, %s, %s)
            """, (nombre, email, fecha_hora, mesa_id))
            conn.commit()

            
            cursor.execute("SELECT numero FROM mesas WHERE id = %s", (mesa_id,))
            numero_mesa = cursor.fetchone()[0]

            messagebox.showinfo("Éxito", f"¡Reservación confirmada en la mesa {numero_mesa} para {fecha_hora}!")
            
            
            enviar_correo_confirmacion(email, nombre, fecha_hora, numero_mesa)
            
        else:
            messagebox.showerror("Error", "No hay mesas disponibles para esa fecha y hora.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error de base de datos: {err}")


def consultar_reservacion():
    email = entry_consulta_email.get()

    if not email:
        messagebox.showerror("Error", "Debes ingresar un correo electrónico.")
        return

    try:
        cursor.execute("""
            SELECT nombre, fecha_hora, mesa_id FROM reservaciones 
            WHERE email = %s
        """, (email,))
        reservacion = cursor.fetchone()

        if reservacion:
            nombre, fecha_hora, mesa_id = reservacion

            # Obtener el número de la mesa
            cursor.execute("SELECT numero FROM mesas WHERE id = %s", (mesa_id,))
            numero_mesa = cursor.fetchone()[0]

            messagebox.showinfo("Reservación encontrada", f"Nombre: {nombre}\nFecha y hora: {fecha_hora}\nMesa: {numero_mesa}")
        else:
            messagebox.showinfo("Sin resultados", "No se encontró ninguna reservación con ese correo electrónico.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error de base de datos: {err}")


def modificar_reservacion():
    email = entry_modificar_email.get()
    nueva_fecha_hora = entry_nueva_fecha_hora.get()

    if not email or not nueva_fecha_hora:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    try:
       
        cursor.execute("SELECT id FROM reservaciones WHERE email = %s", (email,))
        reservacion = cursor.fetchone()

        if reservacion:
            reservacion_id = reservacion[0]

            
            cursor.execute("""
                SELECT id FROM mesas 
                WHERE id NOT IN (SELECT mesa_id FROM reservaciones WHERE fecha_hora = %s)
                LIMIT 1
            """, (nueva_fecha_hora,))
            nueva_mesa = cursor.fetchone()

            if nueva_mesa:
                nueva_mesa_id = nueva_mesa[0]

               
                cursor.execute("""
                    UPDATE reservaciones
                    SET fecha_hora = %s, mesa_id = %s
                    WHERE id = %s
                """, (nueva_fecha_hora, nueva_mesa_id, reservacion_id))
                conn.commit()
                messagebox.showinfo("Éxito", "Reservación modificada exitosamente.")
            else:
                messagebox.showerror("Error", "No hay mesas disponibles para la nueva fecha y hora.")
        else:
            messagebox.showerror("Error", "No se encontró una reservación con ese correo electrónico.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error de base de datos: {err}")


def eliminar_reservacion():
    email = entry_eliminar_email.get()

    if not email:
        messagebox.showerror("Error", "Debes ingresar un correo electrónico.")
        return

    try:
        cursor.execute("SELECT id FROM reservaciones WHERE email = %s", (email,))
        reservacion = cursor.fetchone()

        if reservacion:
            cursor.execute("DELETE FROM reservaciones WHERE email = %s", (email,))
            conn.commit()
            messagebox.showinfo("Éxito", "Reservación eliminada exitosamente.")
        else:
            messagebox.showinfo("Sin resultados", "No se encontró ninguna reservación con ese correo electrónico.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error de base de datos: {err}")


def enviar_correo_confirmacion(destinatario, nombre, fecha_hora, numero_mesa):
    remitente = "pruebaprogramacion005@gmail.com"  
    contraseña = "wxtkasvekthlnytg"      
    msg = EmailMessage()
    msg["Subject"] = "Confirmación de reservación"
    msg["From"] = remitente
    msg["To"] = destinatario
    msg.set_content(
        f"Hola {nombre},\n\n"
        f"Tu reservación ha sido confirmada para el día y hora: {fecha_hora}.\n"
        f"Se te ha asignado la mesa número: {numero_mesa}.\n\n"
        f"¡Gracias por reservar con nosotros!"
    )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(remitente, contraseña)
            smtp.send_message(msg)
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        


root = tk.Tk()
root.title("Sistema de Reservaciones")


tk.Label(root, text="Nombre:").grid(row=0, column=0)
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=0, column=1)

tk.Label(root, text="Email:").grid(row=1, column=0)
entry_email = tk.Entry(root)
entry_email.grid(row=1, column=1)

tk.Label(root, text="Fecha y Hora (YYYY-MM-DD HH:MM:SS):").grid(row=2, column=0)
entry_fecha_hora = tk.Entry(root)
entry_fecha_hora.grid(row=2, column=1)

btn_reservar = tk.Button(root, text="Reservar", command=reservar)
btn_reservar.grid(row=3, column=0, columnspan=2, pady=10)


tk.Label(root, text="Consultar reservación por Email:").grid(row=4, column=0)
entry_consulta_email = tk.Entry(root)
entry_consulta_email.grid(row=4, column=1)

btn_consultar = tk.Button(root, text="Consultar", command=consultar_reservacion)
btn_consultar.grid(row=5, column=0, columnspan=2, pady=10)


tk.Label(root, text="Email de reservación a modificar:").grid(row=6, column=0)
entry_modificar_email = tk.Entry(root)
entry_modificar_email.grid(row=6, column=1)

tk.Label(root, text="Nueva Fecha y Hora (YYYY-MM-DD HH:MM:SS):").grid(row=7, column=0)
entry_nueva_fecha_hora = tk.Entry(root)
entry_nueva_fecha_hora.grid(row=7, column=1)

btn_modificar = tk.Button(root, text="Modificar", command=modificar_reservacion)
btn_modificar.grid(row=8, column=0, columnspan=2, pady=10)


tk.Label(root, text="Email de reservación a eliminar:").grid(row=9, column=0)
entry_eliminar_email = tk.Entry(root)
entry_eliminar_email.grid(row=9, column=1)

btn_eliminar = tk.Button(root, text="Eliminar", command=eliminar_reservacion)
btn_eliminar.grid(row=10, column=0, columnspan=2, pady=10)

root.mainloop()
