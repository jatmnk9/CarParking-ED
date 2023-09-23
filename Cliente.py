class Cliente:
    def __init__(self, idCliente, nombre, contacto):
        self.__idCliente = idCliente
        self.__nombre = nombre
        self.__contacto = contacto

    # Getter para el atributo idCliente
    def get_idCliente(self):
        return self.__idCliente

    # Setter para el atributo idCliente
    def set_idCliente(self, idCliente):
        self.__idCliente = idCliente

    # Getter para el atributo nombre
    def get_nombre(self):
        return self.__nombre

    # Setter para el atributo nombre
    def set_nombre(self, nombre):
        self.__nombre = nombre

    # Getter para el atributo contacto
    def get_contacto(self):
        return self.__contacto

    # Setter para el atributo contacto
    def set_contacto(self, contacto):
        self.__contacto = contacto



