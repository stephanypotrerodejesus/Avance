import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import mysql.connector
from datetime import datetime

# Conexión a la base de datos MySQL
def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Cambia estos datos según tu configuración
        password="",  # Cambia estos datos según tu configuración
        database="reservaciones_db"
    )

# Función para verificar disponibilidad
def verificar_disponibilidad():
    fecha_seleccionada = cal.get_date()
    hora_seleccionada = hora_var.get()
    fecha_hora = f"{fecha_seleccionada} {hora_seleccionada}:00"

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM reservaciones WHERE fecha_hora = %s", (fecha_hora,))
    reservadas = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM mesas")
    total_mesas = cursor.fetchone()[0]

    conn.close()

    if reservadas < total_mesas:
        messagebox.showinfo("Disponibilidad", "¡Hay mesas disponibles para esta fecha y hora!")
    else:
        messagebox.showwarning("Sin disponibilidad", "No hay mesas disponibles en este horario.")

# Función para realizar la reservación
def hacer_reservacion():
    nombre = nombre_entry.get()
    email = email_entry.get()
    fecha_seleccionada = cal.get_date()
    hora_seleccionada = hora_var.get()
    fecha_hora = f"{fecha_seleccionada} {hora_seleccionada}:00"

    if not nombre or not email:
        messagebox.showerror("Error", "Por favor, complete todos los campos.")
        return

    conn = conectar_bd()
    cursor = conn.cursor()
    
    # Obtener una mesa disponible
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
        messagebox.showinfo("Éxito", f"¡Reservación confirmada en la mesa {mesa_id} para {fecha_hora}!")
    else:
        messagebox.showwarning("Sin disponibilidad", "No hay mesas disponibles en este horario.")

    conn.close()

# Función para consultar la reservación
def consultar_reservacion():
    email = email_entry.get()

    if not email:
        messagebox.showerror("Error", "Por favor, ingrese un correo electrónico.")
        return

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nombre, fecha_hora, mesa_id FROM reservaciones 
        WHERE email = %s
    """, (email,))
    
    reservacion = cursor.fetchone()

    if reservacion:
        nombre, fecha_hora, mesa_id = reservacion
        messagebox.showinfo("Reservación encontrada", f"Nombre: {nombre}\nFecha y hora: {fecha_hora}\nMesa: {mesa_id}")
    else:
        messagebox.showwarning("No encontrada", "No se encontró una reservación para ese correo electrónico.")
    
    conn.close()

# Función para modificar la reservación
def modificar_reservacion():
    email = email_entry.get()
    nueva_fecha = cal.get_date()
    nueva_hora = hora_var.get()
    nueva_fecha_hora = f"{nueva_fecha} {nueva_hora}:00"

    if not email:
        messagebox.showerror("Error", "Por favor, ingrese un correo electrónico.")
        return

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM reservaciones WHERE email = %s
    """, (email,))
    
    reservacion = cursor.fetchone()

    if reservacion:
        mesa_id = reservacion[0]
        
        cursor.execute("""
            UPDATE reservaciones
            SET fecha_hora = %s
            WHERE email = %s
        """, (nueva_fecha_hora, email))
        
        conn.commit()
        messagebox.showinfo("Éxito", f"¡Reservación modificada para la nueva fecha y hora {nueva_fecha_hora}!")
    else:
        messagebox.showwarning("No encontrada", "No se encontró una reservación para ese correo electrónico.")
    
    conn.close()

# Función para eliminar la reservación
def eliminar_reservacion():
    email = email_entry.get()

    if not email:
        messagebox.showerror("Error", "Por favor, ingrese un correo electrónico.")
        return

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM reservaciones WHERE email = %s
    """, (email,))
    
    reservacion = cursor.fetchone()

    if reservacion:
        cursor.execute("""
            DELETE FROM reservaciones WHERE email = %s
        """, (email,))
        
        conn.commit()
        messagebox.showinfo("Éxito", "¡Reservación eliminada correctamente!")
    else:
        messagebox.showwarning("No encontrada", "No se encontró una reservación para ese correo electrónico.")
    
    conn.close()

# Crear la ventana principal
root = tk.Tk()
root.title("Sistema de Reservaciones")

# Widgets de la interfaz gráfica
tk.Label(root, text="Nombre:").grid(row=0, column=0, padx=10, pady=5)
nombre_entry = tk.Entry(root)
nombre_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Correo:").grid(row=1, column=0, padx=10, pady=5)
email_entry = tk.Entry(root)
email_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Fecha:").grid(row=2, column=0, padx=10, pady=5)
cal = Calendar(root, selectmode="day", date_pattern="yyyy-mm-dd")
cal.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Hora:").grid(row=3, column=0, padx=10, pady=5)
hora_var = tk.StringVar(value="13:00")
horas_disponibles = ["13:00", "14:00", "19:00"]
hora_menu = tk.OptionMenu(root, hora_var, *horas_disponibles)
hora_menu.grid(row=3, column=1, padx=10, pady=5)

# Botones de acción
verificar_btn = tk.Button(root, text="Verificar Disponibilidad", command=verificar_disponibilidad)
verificar_btn.grid(row=4, column=0, columnspan=2, pady=5)

reservar_btn = tk.Button(root, text="Reservar", command=hacer_reservacion)
reservar_btn.grid(row=5, column=0, columnspan=2, pady=5)

consultar_btn = tk.Button(root, text="Consultar Reserva", command=consultar_reservacion)
consultar_btn.grid(row=6, column=0, columnspan=2, pady=5)

modificar_btn = tk.Button(root, text="Modificar Reserva", command=modificar_reservacion)
modificar_btn.grid(row=7, column=0, columnspan=2, pady=5)

eliminar_btn = tk.Button(root, text="Eliminar Reserva", command=eliminar_reservacion)
eliminar_btn.grid(row=8, column=0, columnspan=2, pady=10)

root.mainloop()
