from typing import List, Dict, Any, Optional
from PySide6.QtCore import Slot
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QWidget
from utils import utils_db
from utils.utils_popup import _printv2
from models.report_model import ReportModel
from views.report_view import ReportView


class ReportController:
    """
    Controlador para gestionar la interacción entre modelo, vista y base de datos.
    """

    def __init__(self, report_view: ReportView, report_model: ReportModel, popup_parent: Optional[QWidget] = None):
        """
        Inicializa el controlador.

        Parámetros:
        - report_view (ReportView): Vista para la interfaz de usuario.
        - report_model (ReportModel): Modelo de datos.
        - popup_parent (QWidget | None): Padre opcional para los popups.
        """
        if not report_view or not report_model:
            raise ValueError(
                "Se requieren tanto la vista como el modelo para inicializar el controlador.")

        self._view = report_view
        self._model = report_model
        self._popup_parent = popup_parent

        # Conectar señales
        self._view.apply_filters_signal.connect(self._apply_filters)

        # Inicializar vista
        self._initialize_view()

    def _initialize_view(self) -> None:
        """
        Inicializa la vista cargando datos y configurando géneros.
        """
        try:
            # Cargar datos iniciales de videojuegos
            model_data = self._model._get_model(
                utils_db.EnumTablasDB.VIDEOJUEGOS.value)
            if model_data:
                prepared_data = self._prepare_table_data(model_data)
                self._view._set_model(prepared_data)

                # Configurar gráfico inicial
                chart_data = self._prepare_chart_data(model_data)
                self._view._set_chart(chart_data)
            else:
                _printv2(show_popup=False, parent=self._popup_parent,
                         message="No se encontraron datos en la tabla 'videojuegos'.")
                self._view._clear_chart()

            # Cargar géneros
            genres_data : Optional[List[Dict[str,Any]]]=self._model._fetch_data(utils_db.EnumTablasDB.GENEROS.value)
            
            
            if genres_data :
                genres = [row["nombre_genero"] for row in genres_data]
                self._view._set_genres(["Todos"] + genres)
                
            else:
                _printv2(show_popup=False, parent=self._popup_parent,
                         message="No se encontraron datos en la tabla generos")
                
            

        except Exception as e:
            _printv2(show_popup=False, parent=self._popup_parent,
                     message=f"Error al inicializar la vista: {e}")

    @Slot(str, str)
    def _apply_filters(self, search_text: str, genre: str) -> None:
        """
        Aplica los filtros ingresados desde la vista.

        Parámetros:
        - search_text (str): Texto ingresado en la barra de búsqueda.
        - genre (str): Género seleccionado.
        """
        try:
            # Obtener datos de videojuegos
            model_data = self._model._fetch_data(
                utils_db.EnumTablasDB.VIDEOJUEGOS.value)

            if not model_data:
                _printv2(show_popup=False, parent=self._popup_parent,
                         message="No se encontraron datos para aplicar filtros.")
                self._view._clear_chart()
                self._view._set_model(QStandardItemModel())
                self._view._update_summary(0, 0.0)
                return
            
            genres_data = self._model._fetch_data(utils_db.EnumTablasDB.GENEROS.value)
            id_to_genres = {row["id_genero"]: row["nombre_genero"] for row in genres_data} if genres_data else {}

            for row in model_data:
                row["genero"] = id_to_genres.get(row["id_genero"], "Desconocida")

            
            

            # Filtrar por texto de búsqueda y género
            filtered_data = [
                row for row in model_data
                if any(search_text.lower() in str(value).lower() for value in row.values())
                and (genre == "Todos" or row["genero"] == genre)
            ]

            # Calcular resumen
            total_games = len(filtered_data)
            total_ventas = 0
            for row in filtered_data:
                total_ventas += int (row["ventas"])

            # Actualizar resumen en la vista
            # No hay precios en VideojuegoEntity
            self._view._update_summary(total_games, total_ventas)

            # Actualizar tabla
            prepared_data = self._prepare_table_data({
                "columns": ["titulo", "genero", "plataforma","ventas", "fecha_lanzamiento", "descripcion"],
                "data": filtered_data,
            })
            self._view._set_model(prepared_data)

            # Actualizar gráfico
            chart_data = self._prepare_chart_data({
                utils_db.EnumEjes.EJE_X.value: [row["titulo"] for row in filtered_data],
                utils_db.EnumEjes.EJE_Y.value: {"Ventas": [int(row["ventas"]) for row in filtered_data] if filtered_data else []},
            })
            self._view._set_chart(chart_data)

        except Exception as e:
            _printv2(show_popup=False, parent=self._popup_parent,
                     message=f"Error al aplicar filtros: {e}")

    def _prepare_table_data(self, model_data: Dict[str, Any]) -> QStandardItemModel:
        """
        Prepara los datos para el modelo de tabla.

        Parámetros:
        - model_data (dict): Datos de la tabla.

        Retorno:
        - QStandardItemModel: Modelo para la tabla.
        """
        qt_model = QStandardItemModel()
        columns = model_data.get("columns", [])
        qt_model.setHorizontalHeaderLabels(columns)

        for row in model_data.get("data", []):
            items = [QStandardItem(str(row.get(col, ""))) for col in columns]
            qt_model.appendRow(items)

        return qt_model

    def _prepare_chart_data(self, model_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepara los datos estructurados para graficar.

        Parámetros:
        - model_data (dict): Datos estructurados.

        Retorno:
        - dict: Datos para el gráfico.
        """
        eje_x = model_data.get(utils_db.EnumEjes.EJE_X.value, [])
        eje_y = model_data.get(utils_db.EnumEjes.EJE_Y.value, {})

        return {
            utils_db.EnumEjes.EJE_X.value: eje_x,
            utils_db.EnumEjes.EJE_Y.value: eje_y,
        }
