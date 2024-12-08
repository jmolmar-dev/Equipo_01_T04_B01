# Archivo: src/models/genero_entity.py

class GeneroEntity:
    """
    Clase que representa un género en la aplicación.
    Cada instancia corresponde a un registro en la tabla `generos` de la base de datos.

    Métodos disponibles:
    - _to_dict(): Convierte la instancia en un diccionario para facilitar la manipulación de datos.
    - _from_dict(data): Crea una instancia de GeneroEntity a partir de un diccionario.
    - __str__(): Representación legible para humanos.
    - __repr__(): Representación técnica detallada del objeto.
    - __eq__(): Compara dos géneros basándose en su atributo 'id_genero'.
    - __hash__(): Genera un hash único basado en 'id_genero'.
    """

    def __init__(self, id_genero, nombre_genero):
        """
        Inicializa un objeto GeneroEntity con los datos de un género.

        Parámetros:
        - id_genero (int): ID único del género.
        - nombre_genero (str): Nombre descriptivo del género (e.g., Aventura, RPG, Acción).
        """
        self._id_genero = id_genero
        self._nombre_genero = nombre_genero
    # __init__ (fin)

    def _to_dict(self):
        """
        Convierte la instancia actual en un diccionario.

        Retorno:
        - dict: Representación del género como un diccionario.
        """
        return {
            "id_genero": self._id_genero,
            "nombre_genero": self._nombre_genero
        }
    # _to_dict (fin)

    @classmethod
    def _from_dict(cls, data):
        """
        Crea una instancia de GeneroEntity a partir de un diccionario.

        Parámetros:
        - data (dict): Diccionario con los datos del género.

        Retorno:
        - GeneroEntity: Instancia creada con los datos proporcionados.
        """
        return cls(
            id_genero=data.get("id_genero"),
            nombre_genero=data.get("nombre_genero")
        )
    # _from_dict (fin)

    def __str__(self):
        """
        Devuelve una representación legible del género.

        Retorno:
        - str: Representación en formato legible.
        """
        return f"Género: {self._nombre_genero} (ID: {self._id_genero})"
    # __str__ (fin)

    def __repr__(self):
        """
        Devuelve una representación técnica del género.

        Retorno:
        - str: Representación en formato técnico.
        """
        return f"GeneroEntity(id_genero={self._id_genero}, nombre_genero='{self._nombre_genero}')"
    # __repr__ (fin)

    def __eq__(self, other):
        """
        Comprueba si dos instancias de GeneroEntity son iguales, basándose en su ID.

        Parámetros:
        - other (GeneroEntity): Otra instancia a comparar.

        Retorno:
        - bool: True si los IDs son iguales, False en caso contrario.
        """
        if not isinstance(other, GeneroEntity):
            return False
        return self._id_genero == other._id_genero
    # __eq__ (fin)

    def __hash__(self):
        """
        Devuelve el hash de la instancia, basado en su ID.

        Retorno:
        - int: Valor hash de la instancia.
        """
        return hash(self._id_genero)
    # __hash__ (fin)
# GeneroEntity (fin)
