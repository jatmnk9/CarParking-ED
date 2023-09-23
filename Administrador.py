class Administrador:
    def __init__(self, usuario, contrasenia, llaveMaestra):
        self.__usuario = usuario
        self.__contrasenia = contrasenia
        self.__llaveMaestra = llaveMaestra

    # Getter para el atributo usuario
    def get_usuario(self):
        return self.__usuario

    # Setter para el atributo usuario
    def set_usuario(self, usuario):
        self.__usuario = usuario

    # Getter para el atributo contrasenia
    def get_contrasenia(self):
        return self.__contrasenia

    # Setter para el atributo contrasenia
    def set_contrasenia(self, contrasenia):
        self.__contrasenia = contrasenia

    # Getter para el atributo llaveMaestra
    def get_llaveMaestra(self):
        return self.__llaveMaestra

    # Setter para el atributo llaveMaestra
    def set_llaveMaestra(self, llaveMaestra):
        self.__llaveMaestra = llaveMaestra

