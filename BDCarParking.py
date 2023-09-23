import sqlite3 as sql

nombreBD = "BDCarParking.db"

def createDB():
    conn = sql.connect(nombreBD)
    conn.commit()
    conn.close()

def createTableVehiculos():
    conn=sql.connect(nombreBD)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE Vehiculos(
         idVehiculo integer,
         nombreCliente text,
         placa text,
         tipo text
        )"""   
    )
    conn.commit()
    conn.close()

def insertRowVehiculos(idVehiculo,nombreCliente,placa,tipo):
    conn = sql.connect(nombreBD)
    cursor = conn.cursor()
    instruction = f"INSERT INTO Vehiculos VALUES ({idVehiculo},'{nombreCliente}','{placa}','{tipo}')"
    cursor.execute(instruction)
    conn.commit()
    conn.close()

def createTableClientes():
    conn=sql.connect(nombreBD)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE Clientes(
         idCliente integer,
         nombre text,
         contacto text
        )"""   
    )
    conn.commit()
    conn.close()

def insertRowClientes(idCliente,nombre,contacto):
    conn = sql.connect(nombreBD)
    cursor = conn.cursor()
    instruction = f"INSERT INTO Clientes VALUES ({idCliente},'{nombre}','{contacto}')"
    cursor.execute(instruction)
    conn.commit()
    conn.close()

def createTableAdministradores():
    conn=sql.connect(nombreBD)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE Administradores(
         usuario text,
         contrasenia text,
         llaveMaestra integer
        )"""   
    )
    conn.commit()
    conn.close()

def insertRowAdministradores(usuario,contrasenia,llaveMaestra):
    conn = sql.connect(nombreBD)
    cursor = conn.cursor()
    instruction = f"INSERT INTO Administradores VALUES ('{usuario}','{contrasenia}',{llaveMaestra})"
    cursor.execute(instruction)
    conn.commit()
    conn.close()

def createTableTickets():
    conn=sql.connect(nombreBD)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE Tickets(
         idTicket integer,
         nombreCliente text,
         horaIngreso text,
         horaSalida text,
         fecha text,
         placaVehiculo text,
         ubicacion integer,
         monto real,
         horasTotales real
        )"""   
    )
    conn.commit()
    conn.close()

def insertRowTickets(idTicket,nombreCliente,horaIngreso,horaSalida,fecha,placaVehiculo,ubicacion,monto,horasTotales):
    conn = sql.connect(nombreBD)
    cursor = conn.cursor()
    instruction = f"INSERT INTO Tickets VALUES ({idTicket},'{nombreCliente}','{horaIngreso}','{horaSalida}','{fecha}','{placaVehiculo}',{ubicacion},{monto},{horasTotales})"
    cursor.execute(instruction)
    conn.commit()
    conn.close()


def limpiarTable(tabla):
    conn = sql.connect(nombreBD)
    cursor = conn.cursor()
    cursor.execute(
        """
        DELETE FROM   {}
        """.format(tabla)
    )
    conn.commit()
    conn.close()

#limpiarTable("Clientes")
#limpiarTable("Tickets")
#limpiarTable("Vehiculos")
#createDB()
#createTableClientes()
#createTableTickets()
#createTableVehiculos()
#createTableAdministradores()
#insertRowAdministradores("Rose","rose1",1)
#insertRowAdministradores("Jennie","jennie1",2)
#insertRowClientes(1234567,"Camila Cabello","camila@gmail.com")
#insertRowVehiculos(789456,"Camila Cabello","ABC123","Camioneta")
#insertRowTickets(3698527,"Camila Cabello","15:04:05","16:06:16","15-06-2023","ABC123",0,12,1)
#insertRowTickets(3698527,"Camila Cabello","15:04:05","16:06:16","15-01-2023","ABC123",0,12,1)
#insertRowTickets(1234567,"Juan Perez","09:30:00","10:45:30","22-01-2023","XYZ789",1,25,3)
#insertRowTickets(9876543,"Maria Gomez","12:15:10","14:30:45","05-01-2023","DEF456",0,8,2)
#insertRowTickets(2468135,"Pedro Rodriguez","17:45:20","18:20:55","11-01-2023","GHI987",1,50,5)


conn = sql.connect(nombreBD)
cursor = conn.cursor()
cursor.execute(
        """
        select sum(monto) from Tickets where fecha like "%/2022%"  
        """
    )
info = cursor.fetchall()
print(info)
conn.commit()
conn.close()

"""
import random
import string
from datetime import datetime, timedelta

# Generar un ID de ticket aleatorio
def generar_id_ticket():
    return random.randint(100000, 999999)

# Generar un monto aleatorio con dos decimales exactos
def generar_monto():
    return round(random.uniform(0, 100), 2)

# Lista de nombres reales para los clientes
nombres_clientes = ["John Doe", "Jane Smith", "Michael Johnson", "Emily Davis", "David Wilson", "Sarah Martinez", "Brian Taylor", "Olivia Anderson", "William Thomas", "Sophia Brown"]

# Generar tickets para cada mes del año 
for mes in range(1, 13):
    for _ in range(30):
        idTicket = generar_id_ticket()
        nombreCliente = random.choice(nombres_clientes)
        fecha = datetime(2021, mes, 1).strftime("%d/%m/%Y")
        horaIngreso = datetime(2021, mes, random.randint(1, 28), random.randint(0, 23), random.randint(0, 59), 0).strftime("%d/%m/%Y %H:%M:%S")
        horaSalida = (datetime.strptime(horaIngreso, "%d/%m/%Y %H:%M:%S") + timedelta(hours=random.randint(1, 4))).strftime("%d/%m/%Y %H:%M:%S")
        placaVehiculo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        ubicacion = 0
        monto = generar_monto()
        horasTotales = random.randint(1, 4)

        insertRowTickets(idTicket, nombreCliente, horaIngreso, horaSalida, fecha, placaVehiculo, ubicacion, monto, horasTotales)
        print(f"insertRowTickets({idTicket}, \"{nombreCliente}\", \"{horaIngreso}\", \"{horaSalida}\", \"{fecha}\", \"{placaVehiculo}\", {ubicacion}, {monto}, {horasTotales})")

"""