class Ticket:
    def __init__(self, idTicket, horaIngreso, horaSalida, fecha, vehiculo, ubicacion, monto, horasTotales):
        self.__idTicket = idTicket
        self.__horaIngreso = horaIngreso
        self.__horaSalida = horaSalida
        self.__fecha = fecha
        self.__vehiculo = vehiculo
        self.__ubicacion = ubicacion
        self.__monto = monto
        self.__horasTotales = horasTotales

    # Getter para el atributo idTicket
    def get_idTicket(self):
        return self.__idTicket

    # Setter para el atributo idTicket
    def set_idTicket(self, idTicket):
        self.__idTicket = idTicket

    # Getter para el atributo horaIngreso
    def get_horaIngreso(self):
        return self.__horaIngreso

    # Setter para el atributo horaIngreso
    def set_horaIngreso(self, horaIngreso):
        self.__horaIngreso = horaIngreso

    # Getter para el atributo horaSalida
    def get_horaSalida(self):
        return self.__horaSalida

    # Setter para el atributo horaSalida
    def set_horaSalida(self, horaSalida):
        self.__horaSalida = horaSalida

    # Getter para el atributo fecha
    def get_fecha(self):
        return self.__fecha

    # Setter para el atributo fecha
    def set_fecha(self, fecha):
        self.__fecha = fecha

    # Getter para el atributo ubicacion
    def get_ubicacion(self):
        return self.__ubicacion

    # Setter para el atributo ubicacion
    def set_ubicacion(self, ubicacion):
        self.__ubicacion = ubicacion

    # Getter para el atributo vehiculo
    def get_vehiculo(self):
        return self.__vehiculo

    # Setter para el atributo vehiculo
    def set_vehiculo(self, vehiculo):
        self.__vehiculo = vehiculo

    # Getter para el atributo monto
    def get_monto(self):
        return self.__monto

    # Setter para el atributo monto
    def set_monto(self, monto):
        self.__monto = monto

    # Getter para el atributo horasTotales
    def get_horasTotales(self):
        return self.__horasTotales

    # Setter para el atributo horasTotales
    def set_horasTotales(self, horasTotales):
        self.__horasTotales = horasTotales
