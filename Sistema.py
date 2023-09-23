from Administrador import Administrador
from Cliente import Cliente
from Ticket import Ticket
from Vehiculo import Vehiculo
import numpy as np
import sqlite3 as sql
import random
import tkinter as tk
import calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
from datetime import datetime
from datetime import date
from tkinter import ttk

nombreBD = "BDCarParking.db"

class Sistema:
    def __init__(self, estado):
        self.__estado = estado

    def get_tarifas():
        tarifas = [2.50, 4.50, 6.50]
        return tarifas

    # Setter para el atributo estado
    def set_estado(self, estado):
        self.__estado = estado

    def generarIdAleatorio():
    # Generar un número entero aleatorio de 7 dígitos
        idAleatorio = int(random.randint(1000000, 9999999))
        return idAleatorio
    

    def obtenerFechaHoraActual():
        # Obtener la fecha y hora actual
        fecha_hora_actual = datetime.now()
        # Formatear la fecha y hora en formato de cadena (dd/mm/aaaa HH:MM:SS)
        fecha_hora_actual_str = fecha_hora_actual.strftime("%d/%m/%Y %H:%M:%S")
        return fecha_hora_actual_str
    
    def obtenerFechaActual():
        # Obtener la fecha actual
        fecha_actual = date.today()

        # Formatear la fecha en formato de cadena (dd/mm/aaaa)
        fecha_actual_str = fecha_actual.strftime("%d/%m/%Y")

        return fecha_actual_str
        
    def registrarCliente(cliente):
        conn = sql.connect(nombreBD)
        cursor = conn.cursor()
        # Insertar los datos del ticket en la tabla Tickets
        cursor.execute(
            "INSERT INTO Clientes (idCliente, nombre, contacto) VALUES (?, ?, ?)",
            (cliente.get_idCliente(),cliente.get_nombre(),cliente.get_contacto())
        )
        conn.commit()
        conn.close()

    def registrarVehiculo(cliente,vehiculo):
        conn = sql.connect(nombreBD)
        cursor = conn.cursor()
        # Insertar los datos del ticket en la tabla Tickets
        cursor.execute(
            "INSERT INTO Vehiculos (idVehiculo, nombreCliente, placa, tipo) VALUES (?, ?, ?, ?)",
            (vehiculo.get_idVehiculo(),cliente.get_nombre(),vehiculo.get_placa(),vehiculo.get_tipo())
        )
        conn.commit()
        conn.close()

    def crearEstacionamiento(): #Matriz y FILA secuencial
        tamanioMatriz = int(input("Ingrese el tamanio del estacionamiento: "))
         # Crear una matriz nxn llena de ceros
        estacionamiento = np.zeros((tamanioMatriz, tamanioMatriz), dtype=int)
        # Guardar la matriz en un archivo
        np.savetxt('estacionamiento.txt', estacionamiento, fmt='%d')
        


    def liberarVehiculo(placa):
        tickets = Sistema.obtenerTicketsPorPlaca(placa)

        if tickets:
            ticket_mas_reciente = max(tickets, key=lambda ticket: ticket.get_horaIngreso())

            for ticket in tickets:
                if ticket == ticket_mas_reciente:
                    # Verificar si el vehículo ya está liberado
                    if ticket.get_horaSalida():
                        tk.messagebox.showerror("Error", "El vehículo ya fue liberado.")
                        return None

                    # Actualizar horaSalida
                    hora_salida = Sistema.obtenerFechaHoraActual()
                    ticket.set_horaSalida(hora_salida)

                    # Calcular horasTotales
                    hora_ingreso = ticket.get_horaIngreso()
                    tiempo_ingreso = datetime.strptime(hora_ingreso, "%d/%m/%Y %H:%M:%S")

                    # Obtener la fecha y hora actual
                    tiempo_salida = datetime.now()

                    # Calcular la diferencia de tiempo
                    diferencia_tiempo = tiempo_salida - tiempo_ingreso

                    # Calcular las horas totales
                    horas_totales = diferencia_tiempo.total_seconds() // 3600
                    ticket.set_horasTotales(horas_totales)

                    # Actualizar monto
                    monto_actualizado = ticket.get_monto() * horas_totales
                    if monto_actualizado == 0:
                        monto_actualizado = ticket.get_monto()
                    ticket.set_monto(monto_actualizado)

                    # Actualizar el ticket en la base de datos
                    conn = sql.connect(nombreBD)
                    cursor = conn.cursor()
                    query = "UPDATE Tickets SET horaSalida=?, horasTotales=?, monto=? WHERE idTicket=?"
                    cursor.execute(query, (ticket.get_horaSalida(), ticket.get_horasTotales(), ticket.get_monto(), ticket.get_idTicket()))
                    conn.commit()
                    conn.close()

                    # Obtener ubicacion del ticket
                    ubicacion_ticket = ticket.get_ubicacion()
                    Sistema.liberarUbicacion(ubicacion_ticket)

                    return ticket

    def imprimirTicket(ticket):
        ventana = tk.Tk()
        ventana.title("Ticket de Salida")
        
        separador = "=" * 20
        
        etiqueta_titulo = tk.Label(ventana, text="ESTACIONAMIENTO MONO", font=("Arial", 12, "bold"))
        etiqueta_titulo.pack()
        
        etiqueta_separador1 = tk.Label(ventana, text=separador)
        etiqueta_separador1.pack()
        
        etiqueta_id = tk.Label(ventana, text=f"ID Ticket: {ticket.get_idTicket()}")
        etiqueta_id.pack()
        
        etiqueta_hora_ingreso = tk.Label(ventana, text=f"Hora Ingreso: {ticket.get_horaIngreso()}")
        etiqueta_hora_ingreso.pack()
        
        etiqueta_hora_salida = tk.Label(ventana, text=f"Hora Salida: {ticket.get_horaSalida()}")
        etiqueta_hora_salida.pack()
        
        etiqueta_fecha = tk.Label(ventana, text=f"Fecha: {ticket.get_fecha()}")
        etiqueta_fecha.pack()
        
        etiqueta_vehiculo = tk.Label(ventana, text=f"Vehículo: {ticket.get_vehiculo().get_placa()}")
        etiqueta_vehiculo.pack()
        
        etiqueta_ubicacion = tk.Label(ventana, text=f"Ubicación: {ticket.get_ubicacion()}")
        etiqueta_ubicacion.pack()
        
        etiqueta_separador2 = tk.Label(ventana, text=separador)
        etiqueta_separador2.pack()
        
        etiqueta_monto = tk.Label(ventana, text=f"Monto a Pagar: S/ {ticket.get_monto()}")
        etiqueta_monto.pack()
        
        etiqueta_horas_totales = tk.Label(ventana, text=f"Horas Totales: {ticket.get_horasTotales()}")
        etiqueta_horas_totales.pack()
        
        etiqueta_separador3 = tk.Label(ventana, text=separador)
        etiqueta_separador3.pack()
        
        etiqueta_gracias = tk.Label(ventana, text="¡Gracias por utilizar nuestro servicio!", font=("Arial", 12, "bold"))
        etiqueta_gracias.pack()
        
        etiqueta_titulo_final = tk.Label(ventana, text="ESTACIONAMIENTO MONO", font=("Arial", 12, "bold"))
        etiqueta_titulo_final.pack()
        
        etiqueta_separador4 = tk.Label(ventana, text=separador)
        etiqueta_separador4.pack()
        
        ventana.mainloop()

    def generarReporteIngresosMensuales():
        # Conectar a la base de datos
        conexion = sql.connect(nombreBD)
        cursor = conexion.cursor()

        # Obtener todos los datos de la tabla "Tickets"
        cursor.execute("SELECT fecha, monto FROM Tickets")
        datos_tickets = cursor.fetchall()

        # Cerrar la conexión a la base de datos
        conexion.close()

        # Calcular los ingresos mensuales
        ingresos_mensuales = defaultdict(int)
        for dato in datos_tickets:
            fecha = datetime.strptime(dato[0], "%d/%m/%Y")
            mes = fecha.strftime("%B")  # Obtener el nombre del mes
            ingreso = dato[1]
            ingresos_mensuales[mes] += ingreso

        # Obtener los nombres de los meses y los ingresos correspondientes
        meses = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        ingresos = [ingresos_mensuales[mes] for mes in meses]

        def actualizarGrafico(mes_seleccionado, anio_seleccionado):
            # Filtrar los datos de la tabla "tickets" para el mes y año seleccionados
            fechas_mes = []
            montos_mes = []

            for dato in datos_tickets:
                fecha = datetime.strptime(dato[0], "%d/%m/%Y")
                mes = fecha.strftime("%B")
                anio = fecha.strftime("%Y")
                if mes == mes_seleccionado and anio == anio_seleccionado:
                    fechas_mes.append(fecha.strftime("%d"))  # Obtener solo el día
                    montos_mes.append(dato[1])

            # Obtener los ingresos mensuales del año seleccionado
            ingresos_mensuales_anio = defaultdict(int)
            for dato in datos_tickets:
                fecha = datetime.strptime(dato[0], "%d/%m/%Y")
                anio = fecha.strftime("%Y")
                if anio == anio_seleccionado:
                    mes = fecha.strftime("%B")
                    ingreso = dato[1]
                    ingresos_mensuales_anio[mes] += ingreso

            # Limpiar el gráfico anterior
            ax.clear()

            # Actualizar el gráfico de barras de ingresos mensuales
            ax.bar(fechas_mes, montos_mes)
            ax.set_title(f'Ingresos Mensuales - {mes_seleccionado} {anio_seleccionado}')
            ax.set_xlabel('Día')
            ax.set_ylabel('Ingreso')
            ax.set_xticklabels(fechas_mes)

            # Mostrar el gráfico actualizado en la ventana
            canvas.draw()

            # Obtener el ingreso total del mes seleccionado y año seleccionado
            ingreso_total = sum(montos_mes)
            etiqueta_ingreso_total.config(text=f'Ingreso Total: ${ingreso_total}')

            # Obtener el ingreso del periodo anterior correspondiente al mes y año seleccionado
            indice_mes = meses.index(mes_seleccionado)
            if mes_seleccionado == 'January':
                etiqueta_ingreso_anterior.config(text='Ingreso periodo anterior: -----')
            elif indice_mes == 0:
                if anios.index(anio_seleccionado) == 0:
                    etiqueta_ingreso_anterior.config(text='Ingreso periodo anterior: -')
                else:
                    anio_anterior = anios[anios.index(anio_seleccionado) - 1]
                    if meses[-1] == "January":
                        etiqueta_ingreso_anterior.config(text='Ingreso periodo anterior: -----')
                    else:
                        ingreso_anterior = ingresos_mensuales_anio[(meses[-1])]
                        etiqueta_ingreso_anterior.config(text=f'Ingreso periodo anterior: ${ingreso_anterior}')
            else:
                mes_anterior = meses[indice_mes - 1]
                ingreso_anterior = ingresos_mensuales_anio[(mes_anterior)]
                etiqueta_ingreso_anterior.config(text=f'Ingreso periodo anterior: ${ingreso_anterior}')

            # Actualizar la etiqueta de periodo con el mes y año seleccionado
            etiqueta_mes_seleccionado.config(text=f'{mes_seleccionado} {anio_seleccionado}')

        # Obtener los años disponibles en los datos
        anios = list(set([datetime.strptime(dato[0], "%d/%m/%Y").strftime("%Y") for dato in datos_tickets]))
        anios.sort()

        # Crear la ventana de reporte de ingresos mensuales
        ventana_reporte = tk.Tk()
        ventana_reporte.title('Reporte de Ingresos Mensuales')

        # Crear menú desplegable para seleccionar el año
        etiqueta_anio = tk.Label(ventana_reporte, text='Seleccione el año:')
        etiqueta_anio.pack()

        anio_seleccionado = tk.StringVar(ventana_reporte)
        anio_seleccionado.set(anios[0])  # Establecer el primer año como opción por defecto

        menu_anio = tk.OptionMenu(ventana_reporte, anio_seleccionado, *anios, command=lambda _: actualizarGrafico(mes_seleccionado.get(), anio_seleccionado.get()))
        menu_anio.pack()

        # Crear menú desplegable para seleccionar el mes
        etiqueta_mes = tk.Label(ventana_reporte, text='Seleccione el mes:')
        etiqueta_mes.pack()

        mes_seleccionado = tk.StringVar(ventana_reporte)
        mes_seleccionado.set(meses[0])  # Establecer el primer mes como opción por defecto

        menu_mes = tk.OptionMenu(ventana_reporte, mes_seleccionado, *meses, command=lambda _: actualizarGrafico(mes_seleccionado.get(), anio_seleccionado.get()))
        menu_mes.pack()

        # Calcular los ingresos del mes seleccionado y filtrar los datos de la tabla "tickets"
        ingresos_mes_seleccionado = ingresos[meses.index(mes_seleccionado.get())]

        # Mostrar los datos de ingresos en etiquetas
        etiqueta_periodo = tk.Label(ventana_reporte, text='Periodo:')
        etiqueta_periodo.pack()

        etiqueta_mes_seleccionado = tk.Label(ventana_reporte, text=f'{mes_seleccionado.get()} {anio_seleccionado.get()}')
        etiqueta_mes_seleccionado.pack()

        etiqueta_ingreso_total = tk.Label(ventana_reporte, text=f'Ingreso Total: ${ingresos_mes_seleccionado}')
        etiqueta_ingreso_total.pack()

        etiqueta_ingreso_anterior = tk.Label(ventana_reporte, text='')
        etiqueta_ingreso_anterior.pack()

        # Crear el gráfico de barras de ingresos mensuales
        fig = plt.Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar([], [])
        ax.set_title('Ingresos Mensuales')
        ax.set_xlabel('Día')
        ax.set_ylabel('Ingreso')

        # Mostrar el gráfico vacío en la ventana
        canvas = FigureCanvasTkAgg(fig, master=ventana_reporte)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Mostrar la ventana de reporte
        ventana_reporte.mainloop()

    def asignarUbicacion():
        # Cargar la matriz de estacionamiento desde el archivo
        estacionamiento = np.loadtxt('estacionamiento.txt', dtype=int)
        # Obtener las dimensiones de la matriz
        n = estacionamiento.shape[0]
        # Buscar una posición vacía en la matriz
        for i in range(n):
            for j in range(n):
                if estacionamiento[i][j] == 0:
                    # Marcar la posición como ocupada (1)
                    estacionamiento[i][j] = 1
                    # Guardar la matriz actualizada en el archivo
                    np.savetxt('estacionamiento.txt', estacionamiento, fmt='%d')
                    # Calcular la ubicación como un número entero único
                    ubicacion = i * n + j
                    # Retornar la ubicación ocupada encontrada
                    return ubicacion

    def liberarUbicacion(ubicacion):
        # Cargar la matriz de estacionamiento desde el archivo
        estacionamiento = np.loadtxt('estacionamiento.txt', dtype=int)
        # Obtener las dimensiones de la matriz
        n = estacionamiento.shape[0]
        # Calcular las coordenadas de la ubicación a liberar
        fila = ubicacion // n
        columna = ubicacion % n
        # Marcar la posición como vacía (0)
        estacionamiento[fila][columna] = 0
        # Guardar la matriz actualizada en el archivo
        np.savetxt('estacionamiento.txt', estacionamiento, fmt='%d')
        
    def devolverstacionamiento():
        # Verificar la existencia del archivo de estacionamiento
        try:
            estacionamiento = np.loadtxt('estacionamiento.txt', dtype=int)
        except IOError:
            print("No se encontro el archivo de estacionamiento.")
            return
        return estacionamiento

    def verEstacionamiento():
        # Verificar la existencia del archivo de estacionamiento
        try:
            estacionamiento = np.loadtxt('estacionamiento.txt', dtype=int)
        except IOError:
            print("No se encontro el archivo de estacionamiento.")
            return
        # Obtener las dimensiones de la matriz de estacionamiento
        filas, columnas = estacionamiento.shape
        # Etiquetas para las filas y columnas
        etiquetas_filas = ['f' + str(i) for i in range(filas)]
        
        # Imprimir la matriz de estacionamiento
        print("Estacionamiento:")
        print(" ", end="")
        print()
        for i, fila in enumerate(estacionamiento):
            print(etiquetas_filas[i], end=": ")
            for valor in fila:
                print(valor, end=" ")
            print()

    def validarAdministrador(administrador):
        usuario = administrador.get_usuario()
        contrasenia = administrador.get_contrasenia()
        llaveMaestra = administrador.get_llaveMaestra()
        conn = sql.connect(nombreBD)
        cursor = conn.cursor()
        query = "SELECT * FROM Administradores WHERE usuario=? AND contrasenia=? AND llaveMaestra=?"
        cursor.execute(query, (usuario, contrasenia, llaveMaestra))
        resultado = cursor.fetchone()
        conn.close()
        if resultado is not None:
            return True
        else:
            return False

    def validarEspacioEstacionamiento():
        pass
    
    def limpiarEstacionamiento():
        # Verificar la existencia del archivo de estacionamiento
        try:
            estacionamiento = np.loadtxt('estacionamiento.txt', dtype=int)
        except IOError:
            print("No se encontró el archivo de estacionamiento.")
            return
        # Llenar la matriz de estacionamiento con ceros
        estacionamiento.fill(0)
        # Guardar la matriz actualizada en el archivo
        np.savetxt('estacionamiento.txt', estacionamiento, fmt='%d')
    
    def imprimirClientes():
        pass

    def iniciarSesion(usuario, contrasenia, llaveMaestra):
        conn = sql.connect(nombreBD)
        cursor = conn.cursor()
        # Consulta para buscar administrador
        try:
            cursor.execute(
                "SELECT * FROM Administradores WHERE usuario = ? AND contrasenia = ? AND llaveMaestra = ?",
                (usuario, contrasenia, llaveMaestra),
            )

            user = cursor.fetchone()

            return user
        except sql.Error as e:
            print("Error al buscar usuario:", str(e))

        return None
    
    def recopilarHistorial():
        fecha_actual = date.today()
        fecha = str(fecha_actual.strftime("%d/%m/%Y"))

        conn = sql.connect(nombreBD)
        cursor = conn.cursor()
        # Consulta para buscar administrador
        try:
            cursor.execute("SELECT * FROM Tickets WHERE fecha = ?", (fecha,))
            results = cursor.fetchall()

            return results
        except sql.Error as e:
            print("Error al buscar", str(e))

        return None

    def obtenerVehiculoPlaca(placaBuscada):
        conn = sql.connect(nombreBD)
        cursor = conn.cursor()
        # Consulta para buscar un vehículo por placa
        query = "SELECT * FROM Vehiculos WHERE placa=?"
        cursor.execute(query, (placaBuscada,))
        resultado = cursor.fetchone()
        conn.close()
        if resultado is not None:
            idVehiculo = resultado[0]
            tipo = resultado[3]
            vehiculo = Vehiculo(idVehiculo,placaBuscada,tipo)
            return vehiculo
        else:
            return None

    def obtenerTicketsPorPlaca(placa):
        conn = sql.connect(nombreBD)
        cursor = conn.cursor()
        # Consulta para buscar tickets por placa
        query = "SELECT * FROM Tickets WHERE placaVehiculo=?"
        cursor.execute(query, (placa,))
        resultados = cursor.fetchall()
        conn.close()
        tickets = []
        if resultados:
            for resultado in resultados:
                idTicket = resultado[0]
                horaIngreso = resultado[2]
                horaSalida = resultado[3]
                fecha = resultado[4]
                ubicacion = resultado[6]
                monto = resultado[7]
                horasTotales = resultado[8]
                vehiculo = Sistema.obtenerVehiculoPlaca(placa)  # Obtener el vehículo asociado al ticket
                ticket = Ticket(idTicket, horaIngreso, horaSalida, fecha, vehiculo, ubicacion, monto, horasTotales)
                tickets.append(ticket)

        return tickets  

    def obtenerClientePorNombre(nombreCliente):
        conn = sql.connect(nombreBD)
        cursor = conn.cursor()
        # Consultar los datos del cliente por su nombre en la tabla Clientes
        cursor.execute("SELECT idCliente, contacto FROM Clientes WHERE nombre = ?", (nombreCliente,))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            idCliente, contacto = resultado
            # Crear un objeto Cliente con los datos obtenidos
            cliente = Cliente(idCliente, nombreCliente, contacto)
            return cliente
        return None
        
    def buscarPlaca(placaBuscada):
        conn = sql.connect(nombreBD)
        cursor = conn.cursor()
        # Consulta para buscar un vehículo por placa
        query = "SELECT * FROM Vehiculos WHERE placa=?"
        cursor.execute(query, (placaBuscada,))
        resultado = cursor.fetchone()
        conn.close()
        if resultado is not None:
            return True
        else:
            return False

    def buscarNombre(nombre):
        conn = sql.connect(nombreBD)
        cursor = conn.cursor()
        # Consulta para buscar un cliente por nombre
        query = "SELECT * FROM Clientes WHERE nombre=?"
        cursor.execute(query, (nombre,))
        resultado = cursor.fetchone()
        conn.close()
        if resultado is not None:
            return True
        else:
            return False
        
    def generarTicket(cliente, vehiculo, ticket,ubicacion):
        conn = sql.connect(nombreBD)
        cursor = conn.cursor()
        # Insertar los datos del ticket en la tabla Tickets
        cursor.execute(
            "INSERT INTO Tickets (idTicket, nombreCliente, horaIngreso, horaSalida, fecha, placaVehiculo, ubicacion, monto, horasTotales) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (ticket.get_idTicket(), cliente.get_nombre(), ticket.get_horaIngreso(), ticket.get_horaSalida(), ticket.get_fecha(), vehiculo.get_placa(), ubicacion, ticket.get_monto(), ticket.get_horasTotales())
        )
        conn.commit()
        conn.close()
  
    def obtenerNombreClientePorPlaca(placaVehiculo):
        conn = sql.connect(nombreBD)
        cursor = conn.cursor()

        # Consultar el nombre del cliente por la placa del vehículo en la tabla Vehiculos
        cursor.execute("SELECT nombreCliente FROM Vehiculos WHERE placa = ?", (placaVehiculo,))
        resultado = cursor.fetchone()

        conn.close()

        if resultado:
            nombreCliente = resultado[0]
            return nombreCliente

        return None
    


    # Conectar a la base de datos y obtener los datos de los tickets
    def obtener_datos_tickets():
        # Conectar a la base de datos
        conexion = sql.connect(nombreBD)
        cursor = conexion.cursor()

        # Obtener todos los datos de la tabla "Tickets"
        cursor.execute("SELECT fecha, monto FROM Tickets")
        datos_tickets = cursor.fetchall()

        # Cerrar la conexión a la base de datos
        conexion.close()

        return datos_tickets

    def generarReporteAnual():
        # Obtener los datos de los tickets
        datos_tickets = Sistema.obtener_datos_tickets()

        # Calcular los ingresos anuales por mes
        ingresos_anuales = defaultdict(lambda: defaultdict(int))
        for dato in datos_tickets:
            fecha = datetime.strptime(dato[0], "%d/%m/%Y")
            anio = fecha.strftime("%Y")  # Obtener el año
            mes = fecha.strftime("%B")  # Obtener el nombre del mes
            ingreso = dato[1]
            ingresos_anuales[anio][mes] += ingreso

        # Obtener los años disponibles
        anios = sorted(ingresos_anuales.keys())

        def actualizarGrafico(anio_seleccionado):
            # Obtener los meses y los ingresos del año seleccionado
            ingresos_meses = ingresos_anuales[anio_seleccionado]
            meses = list(ingresos_meses.keys())
            ingresos = list(ingresos_meses.values())

            # Limpiar el gráfico anterior
            ax.clear()

            # Actualizar el gráfico de barras de ingresos anuales
            ax.bar(meses, ingresos)
            ax.set_title(f'Ingresos Anuales - {anio_seleccionado}')
            ax.set_xlabel('Mes')
            ax.set_ylabel('Ingreso')

            # Ajustar el tamaño de la letra de los meses
            ax.tick_params(axis='x', labelrotation=45, labelsize=5)

            # Mostrar el gráfico actualizado en la ventana
            canvas.draw()

            # Obtener el ingreso total del año seleccionado
            ingreso_total = sum(ingresos)
            etiqueta_ingreso_total.config(text=f'Ingreso Total: ${ingreso_total}')

            # Obtener el ingreso del período anterior
            indice_anio = anios.index(anio_seleccionado)
            if indice_anio == 0:
                etiqueta_ingreso_anterior.config(text='Ingreso año anterior: -')
            else:
                anio_anterior = anios[indice_anio - 1]
                ingreso_anterior = sum(ingresos_anuales[anio_anterior].values())
                etiqueta_ingreso_anterior.config(text=f'Ingreso año anterior: ${ingreso_anterior}')

            # Actualizar el campo de etiqueta "Periodo"
            etiqueta_anio_seleccionado.config(text=anio_seleccionado)

        # Crear la ventana de reporte anual
        ventana_reporte = tk.Tk()
        ventana_reporte.title('Reporte Anual')

        # Crear menú desplegable para seleccionar el año
        etiqueta_anio = tk.Label(ventana_reporte, text='Seleccione el año:')
        etiqueta_anio.pack()

        anio_seleccionado = tk.StringVar(ventana_reporte)
        anio_seleccionado.set(anios[0])  # Establecer el primer año como opción por defecto

        menu_anio = tk.OptionMenu(ventana_reporte, anio_seleccionado, *anios, command=actualizarGrafico)
        menu_anio.pack()

        # Calcular los ingresos del año seleccionado y filtrar los datos de la tabla "tickets"
        ingresos_anio_seleccionado = ingresos_anuales[anio_seleccionado.get()]
        meses_seleccionados = list(ingresos_anio_seleccionado.keys())
        ingresos_seleccionados = list(ingresos_anio_seleccionado.values())

        # Mostrar los datos de ingresos en etiquetas
        etiqueta_periodo = tk.Label(ventana_reporte, text='Año:')
        etiqueta_periodo.pack()

        etiqueta_anio_seleccionado = tk.Label(ventana_reporte, text=f'{anio_seleccionado.get()}')
        etiqueta_anio_seleccionado.pack()

        etiqueta_ingreso_total = tk.Label(ventana_reporte, text=f'Ingreso Total: ${sum(ingresos_seleccionados)}')
        etiqueta_ingreso_total.pack()

        etiqueta_ingreso_anterior = tk.Label(ventana_reporte, text='')
        etiqueta_ingreso_anterior.pack()

        # Crear el gráfico de barras de ingresos anuales
        fig = plt.Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar([], [])
        ax.set_title('Ingresos Anuales')
        ax.set_xlabel('Mes')
        ax.set_ylabel('Ingreso')

        # Mostrar el gráfico vacío en la ventana
        canvas = FigureCanvasTkAgg(fig, master=ventana_reporte)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Mostrar la ventana de reporte
        ventana_reporte.mainloop()

    def generarReporteDiario():
        # Obtener la fecha actual en el formato "dd/mm/yyyy"
        fecha_actual = datetime.now().strftime("%d/%m/%Y")

        # Conectar a la base de datos
        conexion = sql.connect(nombreBD)
        cursor = conexion.cursor()

        # Obtener todos los datos de la tabla "Tickets" para la fecha actual
        cursor.execute("SELECT idTicket, nombreCliente, horaIngreso, horaSalida, placaVehiculo, monto, horasTotales FROM Tickets WHERE fecha = ? ORDER BY horaIngreso ASC", (fecha_actual,))
        datos_tickets = cursor.fetchall()

        # Cerrar la conexión a la base de datos
        conexion.close()

        # Crear la ventana de reporte diario
        ventana_reporte = tk.Tk()
        ventana_reporte.title(f'Reporte Diario - Estacionamiento MONO')

        # Crear la etiqueta de título del reporte
        etiqueta_titulo = ttk.Label(ventana_reporte, text=f'Reporte Diario - {fecha_actual}', font=("Arial", 14, "bold"))
        etiqueta_titulo.pack(padx=10, pady=10)

        # Crear el cuadro de datos
        cuadro_datos = ttk.Treeview(ventana_reporte)
        cuadro_datos["columns"] = ("ID", "Cliente", "Hora de Ingreso", "Hora de Salida", "Placa", "Monto", "Horas Totales")

        # Configurar las columnas
        cuadro_datos.column("#0", width=0, stretch=tk.NO)
        cuadro_datos.column("ID", anchor=tk.CENTER, width=80)
        cuadro_datos.column("Cliente", anchor=tk.W, width=150)
        cuadro_datos.column("Hora de Ingreso", anchor=tk.CENTER, width=100)
        cuadro_datos.column("Hora de Salida", anchor=tk.CENTER, width=100)
        cuadro_datos.column("Placa", anchor=tk.CENTER, width=100)
        cuadro_datos.column("Monto", anchor=tk.CENTER, width=80)
        cuadro_datos.column("Horas Totales", anchor=tk.CENTER, width=100)

        # Configurar encabezados de columna
        cuadro_datos.heading("#0", text="", anchor=tk.CENTER)
        cuadro_datos.heading("ID", text="ID", anchor=tk.CENTER)
        cuadro_datos.heading("Cliente", text="Cliente", anchor=tk.W)
        cuadro_datos.heading("Hora de Ingreso", text="Hora de Ingreso", anchor=tk.CENTER)
        cuadro_datos.heading("Hora de Salida", text="Hora de Salida", anchor=tk.CENTER)
        cuadro_datos.heading("Placa", text="Placa", anchor=tk.CENTER)
        cuadro_datos.heading("Monto", text="Monto", anchor=tk.CENTER)
        cuadro_datos.heading("Horas Totales", text="Horas Totales", anchor=tk.CENTER)

        # Agregar los datos de los tickets a la tabla
        for dato in datos_tickets:
            hora_ingreso = dato[2].split(" ")[1]
            hora_salida = dato[3].split(" ")[1] if dato[3] else ""
            cuadro_datos.insert("", tk.END, text="", values=(dato[0], dato[1], hora_ingreso, hora_salida, dato[4], dato[5], dato[6]))

        cuadro_datos.pack(padx=10, pady=10)

        # Ejecutar la ventana de reporte
        ventana_reporte.mainloop()
 
    
def main():
    # usuario = input()
    # contrasenia = input()
    # llaveMaestra = input()
    # user = Sistema.iniciarSesion(usuario, contrasenia, llaveMaestra)
    # print(user)
    print("Iniciar Sesion")
    sistema = Sistema("activo")
    tarifas = Sistema.get_tarifas() 
    #usuario = input("Usuario: ")
    #contrasenia = input("Contrasenia: ")
    #llaveMaestra = int(input("Llave Maestra: "))
    admin = Administrador("Rose","rose1",1)
    if Sistema.validarAdministrador(admin):
        print("Bienvenido al ESTACIONAMIENTO MONO!")
        opcion = None
        while opcion != 0:
            print("----- Menu -----")
            print("1. Ingresar Vehiculo")
            print("2. Liberar Vehiculo")
            print("3. Ver Estacionamiento Disponible")
            print("4. Ver Reportes")
            print("5. Crear Estacionamiento")
            print("6. Limpiar Estacionamiento")
            print("0. Salir")
            opcion = int(input("Ingrese una opcion: "))
            
            if opcion == 1:
                placaBuscada = input("Ingrese la placa del vehiculo: ")
                placaBuscada = placaBuscada.upper()
                vehiculoEncontrado = Sistema.buscarPlaca(placaBuscada)
                if vehiculoEncontrado == True:
                    #El cliente ya esta en la base de datos
                    idTicket = Sistema.generarIdAleatorio()
                    horaIngreso = Sistema.obtenerFechaHoraActual()
                    horaSalida = ""
                    fecha = Sistema.obtenerFechaActual()
                    monto = 0
                    horasTotales = 0
                    ubicacion = int(Sistema.asignarUbicacion())
                    print(ubicacion)
                    vehiculo = Sistema.obtenerVehiculoPlaca(placaBuscada)
                    tipo = vehiculo.get_tipo()
                    if tipo == "moto":
                        monto = tarifas[0]  # Obtener el valor de la posición 0 del vector de tarifas
                    elif tipo == "auto":
                        monto = tarifas[1]  # Obtener el valor de la posición 1 del vector de tarifas
                    elif tipo == "camioneta":
                        monto = tarifas[2]  # Obtener el valor de la posición 2 del vector de tarifas
                    nombreCliente = Sistema.obtenerNombreClientePorPlaca(placaBuscada)
                    vehiculoTicket = [vehiculo]
                    cliente = Sistema.obtenerClientePorNombre(nombreCliente)
                    ticketNuevo = Ticket(idTicket, horaIngreso, horaSalida, fecha, ubicacion,vehiculoTicket, monto, horasTotales)
                    Sistema.generarTicket(cliente,vehiculo,ticketNuevo,ubicacion)
                else:
                    clienteBuscado = input("Ingrese nombre del cliente: ")
                    clienteEncontrado = Sistema.buscarNombre(clienteBuscado)
                    if clienteEncontrado == True:
                        cliente = Sistema.obtenerClientePorNombre(clienteBuscado)
                        idVehiculo = Sistema.generarIdAleatorio()
                        tipo = input("Ingrese el tipo de vehiculo: ")
                        vehiculo = (Vehiculo(idVehiculo, placaBuscada, tipo))
                        idTicket = Sistema.generarIdAleatorio()
                        horaIngreso = Sistema.obtenerFechaHoraActual()
                        horaSalida = ""
                        fecha = Sistema.obtenerFechaActual()
                        if tipo == "moto":
                            monto = tarifas[0]  # Obtener el valor de la posición 0 del vector de tarifas
                        elif tipo == "auto":
                            monto = tarifas[1]  # Obtener el valor de la posición 1 del vector de tarifas
                        elif tipo == "camioneta":
                            monto = tarifas[2]  # Obtener el valor de la posición 2 del vector de tarifas
                        horasTotales = 0
                        ubicacion = int(Sistema.asignarUbicacion())
                        ticketNuevo = Ticket(idTicket, horaIngreso, horaSalida, fecha, vehiculo,ubicacion, monto, horasTotales)
                        Sistema.registrarVehiculo(cliente,vehiculo)
                        Sistema.generarTicket(cliente,vehiculo,ticketNuevo,ubicacion)
                    else:
                        idCliente = Sistema.generarIdAleatorio()
                        contacto = input("Ingrese contacto: ")
                        idVehiculo = Sistema.generarIdAleatorio()
                        tipo = input("Ingrese el tipo de vehiculo: ").lower()
                        if tipo == "moto":
                            monto = tarifas[0]  # Obtener el valor de la posición 0 del vector de tarifas
                        elif tipo == "auto":
                            monto = tarifas[1]  # Obtener el valor de la posición 1 del vector de tarifas
                        elif tipo == "camioneta":
                            monto = tarifas[2]  # Obtener el valor de la posición 2 del vector de tarifas
                        vehiculo = (Vehiculo(idVehiculo, placaBuscada, tipo))
                        idTicket = Sistema.generarIdAleatorio()
                        horaIngreso = Sistema.obtenerFechaHoraActual()
                        horaSalida = ""
                        fecha = Sistema.obtenerFechaActual()
                        horasTotales = 0
                        ubicacion = int(Sistema.asignarUbicacion())
                        ticketNuevo = Ticket(idTicket, horaIngreso, horaSalida, fecha, vehiculo,ubicacion, monto, horasTotales)
                        cliente = Cliente(idCliente,clienteBuscado,contacto)
                        Sistema.registrarCliente(cliente)
                        Sistema.registrarVehiculo(cliente,vehiculo)
                        Sistema.generarTicket(cliente,vehiculo,ticketNuevo,ubicacion)

            elif opcion == 2:
                placaBuscada = input("Ingrese la placa del vehiculo: ")
                Sistema.liberarVehiculo(placaBuscada)
                pass
            elif opcion == 3:
                Sistema.verEstacionamiento()
            elif opcion == 4:
                 while True:
                    print("\n---- MENU REPORTES ----")
                    print("1. Reporte de Ingresos Diarios")
                    print("2. Reporte de Ingresos Mensuales")
                    print("3. Reporte de Ingresos Anuales")
                    opcion_reporte = int(input("Ingrese una opción: "))
                    if opcion_reporte == 1:
                        Sistema.generarReporteDiario()
                    elif opcion_reporte == 2:
                        Sistema.generarReporteIngresosMensuales()
                    elif opcion_reporte == 3:
                        Sistema.generarReporteAnual()
                    elif opcion_reporte == 4:
                        break
                    else:
                        print("Opción inválida. Intente nuevamente.")
            elif opcion == 5:
                Sistema.crearEstacionamiento()
            elif opcion == 6:
                Sistema.limpiarEstacionamiento()
            elif opcion == 0:
                print("Saliendo del programa...")
            else:
                print("Opcion invalida. Por favor, seleccione una opcion valida.")
            print()
    else:
        print("Credenciales incorrectas.")

if __name__ == "__main__":
    main()