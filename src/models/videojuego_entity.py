class VideojuegoEntity:
    """
    Clase que representa un videojuego en la aplicación.
    Cada instancia corresponde a un registro en la tabla `videojuegos` de la base de datos.

    Métodos disponibles:
    - _to_dict(): Convierte la instancia en un diccionario para facilitar la manipulación de datos.
    - _from_dict(data): Crea una instancia de VideojuegoEntity a partir de un diccionario.
    - __str__(): Representación legible para humanos.
    - __repr__(): Representación técnica detallada del objeto.
    - __eq__(): Compara dos videojuegos basándose en su atributo 'titulo'.
    - __hash__(): Genera un hash único basado en 'titulo'.
    """

    def __init__(self, titulo, genero, plataforma, desarrollador, fecha_lanzamiento, sinopsis):
        """
        Inicializa un objeto VideojuegoEntity con los datos del videojuego.

        Parámetros:
        - titulo (str): Título del videojuego.
        - genero (str): Género del videojuego (e.g., Aventura, RPG).
        - plataforma (str): Plataforma (e.g., PC, PlayStation, Xbox).
        - desarrollador (str): Desarrollador del videojuego.
        - fecha_lanzamiento (str): Fecha de lanzamiento del videojuego.
        - sinopsis (str): Resumen o descripción breve del videojuego.
        """
        self._titulo = titulo
        self._genero = genero
        self._plataforma = plataforma
        self._desarrollador = desarrollador
        self._fecha_lanzamiento = fecha_lanzamiento
        self._sinopsis = sinopsis
    # __init__ (fin)

    def _to_dict(self):
        """
        Convierte la instancia actual en un diccionario.

        Retorno:
        - dict: Representación del videojuego como un diccionario.
        """
        return {
            "titulo": self._titulo,
            "genero": self._genero,
            "plataforma": self._plataforma,
            "desarrollador": self._desarrollador,
            "fecha_lanzamiento": self._fecha_lanzamiento,
            "sinopsis": self._sinopsis,
        }
    # _to_dict (fin)

    @classmethod
    def _from_dict(cls, data):
        """
        Crea una instancia de VideojuegoEntity a partir de un diccionario.

        Parámetros:
        - data (dict): Diccionario con los datos del videojuego.

        Retorno:
        - VideojuegoEntity: Instancia creada con los datos proporcionados.
        """
        return cls(
            titulo=data.get("titulo"),
            genero=data.get("genero"),
            plataforma=data.get("plataforma"),
            desarrollador=data.get("desarrollador"),
            fecha_lanzamiento=data.get("fecha_lanzamiento"),
            sinopsis=data.get("sinopsis"),
        )
    # _from_dict (fin)

    def __str__(self):
        """
        Devuelve una representación legible del videojuego.

        Retorno:
        - str: Representación en formato legible.
        """
        return (
            f"Título: {self._titulo}, Género: {
                self._genero}, Plataforma: {self._plataforma}, "
            f"Desarrollador: {self._desarrollador}, Fecha de Lanzamiento: {
                self._fecha_lanzamiento}, "
            f"Sinopsis: {self._sinopsis}"
        )
    # __str__ (fin)

    def __repr__(self):
        """
        Devuelve una representación técnica del videojuego.

        Retorno:
        - str: Representación en formato técnico.
        """
        return (
            f"VideojuegoEntity(titulo={self._titulo!r}, genero={
                self._genero!r}, "
            f"plataforma={self._plataforma!r}, desarrollador={
                self._desarrollador!r}, "
            f"fecha_lanzamiento={self._fecha_lanzamiento!r}, sinopsis={
                self._sinopsis!r})"
        )
    # __repr__ (fin)

    def __eq__(self, other):
        """
        Comprueba si dos instancias de VideojuegoEntity son iguales, basándose en su título.

        Parámetros:
        - other (VideojuegoEntity): Otra instancia a comparar.

        Retorno:
        - bool: True si los títulos son iguales, False en caso contrario.
        """
        if not isinstance(other, VideojuegoEntity):
            return False
        return self._titulo == other._titulo
    # __eq__ (fin)

    def __hash__(self):
        """
        Devuelve el hash de la instancia, basado en su título.

        Retorno:
        - int: Valor hash de la instancia.
        """
        return hash(self._titulo)
    # __hash__ (fin)
# VideojuegoEntity (fin)
